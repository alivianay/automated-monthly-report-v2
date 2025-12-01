import os
from datetime import datetime
from typing import Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.input_data import DESTINATION_FOLDER_ID, SCREENSHOT_FOLDER_ID
from core.screenshots_utils import screenshot_specific_element_playwright

# --- Konfigurasi Lingkup ---
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

# =========================
# Google Auth & Services
# =========================
def authenticate_google():
    """
    Autentikasi user Google (OAuth) menggunakan token.json/credentials_google.json.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and getattr(creds, "refresh_token", None):
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_google.json", SCOPES
            )
            # port=0 agar otomatis memilih port yang bebas
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_slides_service():
    return build("slides", "v1", credentials=authenticate_google())


def get_drive_service():
    return build("drive", "v3", credentials=authenticate_google())


# =========================
# Google Drive Helpers
# =========================
def upload_to_drive(
    filepath: str,
    filename: str,
    file_type: str = "default",
    folder_id: Optional[str] = None,
) -> str:
    """
    Upload file ke Google Drive.
    - Memastikan file ada sebelum upload (hindari FileNotFoundError).
    - Memilih folder otomatis berdasarkan `file_type` jika `folder_id` tidak diisi.
    - Mengatur permission 'anyone with the link' -> reader.
    """
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(
            f"[upload_to_drive] File tidak ditemukan: {filepath}. "
            "Kemungkinan besar proses screenshot gagal atau path salah."
        )

    drive_service = get_drive_service()

    # Tentukan folder tujuan
    if not folder_id:
        folder_id = SCREENSHOT_FOLDER_ID if file_type == "screenshot" else DESTINATION_FOLDER_ID

    file_metadata = {
        "name": filename if filename.endswith(".png") else f"{filename}.png",
        "mimeType": "image/png",
        "parents": [folder_id],
    }

    media = MediaFileUpload(filepath, mimetype="image/png")
    uploaded = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    file_id = uploaded.get("id")

    # Set permission publik (read-only)
    drive_service.permissions().create(
        fileId=file_id, body={"type": "anyone", "role": "reader"}
    ).execute()

    print(f"☁️ File di-upload ke Google Drive (folder: {folder_id}), file_id = {file_id}")
    return file_id


# =========================
# Google Slides Helpers
# =========================
def copy_slide_template(drive_service, template_slide_id, destination_folder_id, new_file_name) -> str:
    metadata = {
        "name": new_file_name,
        "parents": [destination_folder_id],
        "mimeType": "application/vnd.google-apps.presentation",
    }
    return (
        drive_service.files()
        .copy(fileId=template_slide_id, body=metadata)
        .execute()["id"]
    )


def replace_text_in_google_slide(presentation_id: str, replacements: Dict[str, str]) -> None:
    """
    Ganti seluruh placeholder teks di presentasi.
    - replacements: {"{{PLACEHOLDER}}": "Teks Baru", ...}
    """
    if not replacements:
        print("ℹ️ Tidak ada replacements yang diberikan, skip replace text.")
        return

    slides_service = get_slides_service()
    requests = [
        {
            "replaceAllText": {
                "replaceText": new_text,
                "containsText": {"text": old_text, "matchCase": True},
            }
        }
        for old_text, new_text in replacements.items()
    ]

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()
    print("📝 Placeholder teks berhasil diganti.")


def insert_image_to_slide(
    presentation_id: str,
    image_file_id: str,
    slide_index: int = 0,
    x: float = 50,
    y: float = 50,
    width: float = 600,
    height: float = 340,
) -> None:
    """
    Sisipkan gambar (dari file_id Google Drive) ke slide tertentu.
    Koordinat & ukuran dalam satuan PT (Point).
    """
    slides_service = get_slides_service()
    pres = slides_service.presentations().get(presentationId=presentation_id).execute()
    slides = pres.get("slides", [])
    if slide_index < 0 or slide_index >= len(slides):
        raise IndexError(
            f"[insert_image_to_slide] slide_index {slide_index} di luar range (0..{len(slides)-1})."
        )

    page_id = slides[slide_index]["objectId"]
    image_url = f"https://drive.google.com/uc?id={image_file_id}"

    requests = [
        {
            "createImage": {
                "url": image_url,
                "elementProperties": {
                    "pageObjectId": page_id,
                    "size": {
                        "height": {"magnitude": height, "unit": "PT"},
                        "width": {"magnitude": width, "unit": "PT"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": x,
                        "translateY": y,
                        "unit": "PT",
                    },
                },
            }
        }
    ]

    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={"requests": requests}
    ).execute()
    print("🖼️ Gambar berhasil disisipkan ke slide.")


# =========================
# Orkestrasi: Screenshot -> Upload -> Insert
# =========================
def capture_and_insert_to_slide(
    url: str,
    presentation_id: str,
    slide_index: int = 0,
    selector: Optional[str] = None,
    full_dashboard: bool = True,   # (disimpan bila dipakai oleh caller lain)
    drive_filename: str = "Screenshot Upload",
    x: float = 50,
    y: float = 50,
    width: float = 600,
    height: float = 340,
    wait_time: int = 30,
    tab: Optional[str] = None,
    wait_for: Optional[str] = None,
    drive_folder_id: Optional[str] = None,  # folder custom untuk screenshot
) -> Optional[str]:
    """
    Alur lengkap:
    1) Screenshot elemen dengan Playwright (simpan ke temp/element_YYYYMMDD_HHMMSS.png)
    2) Upload PNG ke Drive (ke folder screenshot/default)
    3) Sisipkan gambar ke slide sesuai koordinat/ukuran

    Mengembalikan file_id Drive (str) jika sukses, atau None bila gagal.
    """
    if not selector:
        raise ValueError(
            "Selector wajib diisi jika ingin screenshot elemen saja. "
            "Jika mau full page, ubah fungsi screenshot untuk mode full."
        )

    # Siapkan path file temporary
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = "temp"
    os.makedirs(out_dir, exist_ok=True)
    filename = f"element_{ts}.png"
    output_file = os.path.join(out_dir, filename)

    # 1) Screenshot (dengan proteksi error)
    try:
        screenshot_specific_element_playwright(
            url,
            selector,
            output_file=output_file,
            wait_time=wait_time,
            tab=tab,
            wait_for=wait_for,
        )
    except Exception as e:
        # Kalau fungsi internal raise, jelaskan kenapa.
        print(
            f"[ERROR] Gagal menjalankan screenshot_specific_element_playwright: {e}\n"
            "Kemungkinan selector tidak match, elemen ada di iframe, perlu klik tab/filter dulu, "
            "atau render data lama (timeout)."
        )
        return None

    # 2) Validasi hasil screenshot: ada & non-empty
    if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
        print(
            f"[INFO] Screenshot tidak ditemukan atau kosong: {output_file}. "
            "Upload & insert slide dibatalkan."
        )
        return None

    # 3) Upload ke Drive
    file_id = None
    try:
        file_id = upload_to_drive(
            output_file,
            drive_filename,
            file_type="screenshot",
            folder_id=drive_folder_id,  # <-- perbaikan: hormati argumen custom folder
        )
    except Exception as e:
        print(f"[ERROR] Upload ke Drive gagal: {e}")
        # Tetap coba hapus file lokal agar bersih
        try:
            os.remove(output_file)
        except Exception:
            pass
        return None

    # 4) Sisipkan ke Slide
    try:
        insert_image_to_slide(
            presentation_id,
            file_id,
            slide_index=slide_index,
            x=x,
            y=y,
            width=width,
            height=height,
        )
    except Exception as e:
        print(f"[ERROR] Insert image ke slide gagal: {e}")
        # Gagal sisipkan gambar bukan berarti upload gagal—tetap kembalikan file_id
        # agar kamu bisa cek file di Drive.
        pass
    finally:
        # 5) Cleanup file lokal (opsional)
        try:
            if os.path.exists(output_file):
                os.remove(output_file)
        except Exception:
            # kalau gagal hapus, tidak fatal
            pass

    return file_id