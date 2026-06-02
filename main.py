from config.input_data import LOOKER_DASHBOARD_URL, TEMPLATE_PRESENTATION_ID, DESTINATION_FOLDER_ID, FILE_NAME, TEXT_REPLACEMENT, ELEMENT_TO_CAPTURE
from core.slide_utils import get_drive_service, copy_slide_template, replace_text_in_google_slide, capture_and_insert_to_slide
from datetime import datetime
import os

if __name__ == "__main__":
    print("\U0001F4C1 Menyalin template ke folder tujuan...")
    drive_service = get_drive_service()
    new_presentation_id = copy_slide_template(drive_service, TEMPLATE_PRESENTATION_ID, DESTINATION_FOLDER_ID, FILE_NAME)
    print(f"Slide baru dibuat dengan ID: {new_presentation_id}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    element_path = os.path.join("output", "screenshots", f"elemen_{timestamp}.png")

    for elem in ELEMENT_TO_CAPTURE:
        capture_and_insert_to_slide(
            url = LOOKER_DASHBOARD_URL, 
            presentation_id = new_presentation_id, 
            slide_index=elem['slide_index'], 
            selector=elem['selector'], 
            full_dashboard=False, 
            drive_filename=f"{elem['title']}_Screenshot", 
            x=elem['x'], 
            y=elem['y'], 
            width=elem['width'], 
            height=elem['height'],
            tab=elem.get('tab'),
            wait_for=elem.get('wait_for'),
        )
    replace_text_in_google_slide(new_presentation_id, TEXT_REPLACEMENT)
    print("Semua proses selesai otomatis.")