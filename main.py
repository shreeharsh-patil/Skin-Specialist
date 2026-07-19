import os
from pathlib import Path

import gradio as gr

from doctor_brain import brain_of_the_doctor
from doctor_voice import convert_text_to_doctor_audio
from patient_voice import transcribe_patient_voice


APP_TITLE = "AI Skin Specialist"
GRADIO_DEBUG = os.environ.get("GRADIO_DEBUG", "true").lower() == "true"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
    --ais-bg: #f7f9fb;
    --ais-surface: #ffffff;
    --ais-surface-low: #f2f4f6;
    --ais-surface-container: #eceef0;
    --ais-border: #c6c6cd;
    --ais-border-strong: #76777d;
    --ais-text: #191c1e;
    --ais-muted: #45464d;
    --ais-primary: #0051d5;
    --ais-primary-soft: #dbe1ff;
    --ais-primary-active: #316bf3;
    --ais-danger: #ba1a1a;
    --ais-danger-soft: #ffdad6;
    --ais-radius: 16px;
    --body-background-fill: #f7f9fb;
    --body-text-color: #191c1e;
    --background-fill-primary: #ffffff;
    --background-fill-secondary: #f2f4f6;
    --block-background-fill: #ffffff;
    --block-border-color: #c6c6cd;
    --block-info-text-color: #45464d;
    --block-label-background-fill: #ffffff;
    --block-label-border-color: #c6c6cd;
    --block-label-text-color: #45464d;
    --input-background-fill: #ffffff;
    --input-background-fill-focus: #ffffff;
    --input-border-color: #c6c6cd;
    --input-border-color-focus: #316bf3;
    --input-placeholder-color: #76777d;
    --button-primary-background-fill: #316bf3;
    --button-primary-background-fill-hover: #0051d5;
    --button-primary-text-color: #fefcff;
    color-scheme: light;
}

.gradio-container {
    background: var(--ais-bg) !important;
    color: var(--ais-text) !important;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif !important;
}

.gradio-container,
.gradio-container * {
    color-scheme: light !important;
}

.ais-shell {
    max-width: 1280px;
    margin: 0 auto;
    padding: 28px 40px 40px;
}

.ais-topbar {
    align-items: center;
    background: var(--ais-surface);
    border: 1px solid var(--ais-border);
    border-radius: 20px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 32px;
    padding: 20px 24px;
}

.ais-brand h1 {
    color: var(--ais-text);
    font-size: 24px;
    font-weight: 650;
    letter-spacing: -0.01em;
    line-height: 32px;
    margin: 0;
}

.ais-brand p,
.ais-footer,
.ais-note,
.ais-panel-copy {
    color: var(--ais-muted);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.03em;
    line-height: 16px;
    margin: 4px 0 0;
}

.ais-security {
    align-items: center;
    color: var(--ais-muted);
    display: flex;
    font-size: 12px;
    font-weight: 600;
    gap: 10px;
}

.ais-security span:not(.ais-icon),
.ais-empty strong,
.ais-panel-copy {
    color: var(--ais-muted) !important;
}

.ais-empty strong {
    color: var(--ais-text) !important;
    display: block;
    font-size: 18px;
    font-weight: 650;
    line-height: 28px;
    margin-bottom: 6px;
}

.ais-icon {
    color: var(--ais-primary);
    font-family: 'Material Symbols Outlined';
    font-size: 22px;
    font-variation-settings: 'FILL' 0, 'wght' 450, 'GRAD' 0, 'opsz' 24;
    line-height: 1;
}

.ais-grid {
    align-items: start;
    display: grid;
    gap: 24px;
    grid-template-columns: minmax(0, 5fr) minmax(0, 7fr);
}

.ais-section-title {
    align-items: center;
    display: flex;
    gap: 8px;
    margin: 0 0 14px;
}

.ais-section-title h2 {
    color: var(--ais-text);
    font-size: 24px;
    font-weight: 650;
    line-height: 32px;
    margin: 0;
}

.ais-card {
    background: var(--ais-surface);
    border: 1px solid var(--ais-border);
    border-radius: var(--ais-radius);
    box-shadow: 0 12px 34px rgba(19, 27, 46, 0.06);
    padding: 20px;
}

.ais-input-card {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.ais-field-label {
    color: var(--ais-muted);
    display: block;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.01em;
    margin-bottom: 12px;
}

.ais-media-row {
    display: grid;
    gap: 16px;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.ais-submit-wrap .gr-button-primary {
    background: var(--ais-primary-active) !important;
    border: 0 !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 24px rgba(0, 81, 213, 0.18) !important;
    color: #fefcff !important;
    font-size: 18px !important;
    font-weight: 650 !important;
    min-height: 64px !important;
}

.ais-submit-wrap .gr-button-primary:hover {
    background: var(--ais-primary) !important;
}

.ais-note {
    align-items: flex-start;
    background: rgba(219, 225, 255, 0.55);
    border-radius: 12px;
    color: #003ea8 !important;
    display: flex;
    gap: 8px;
    padding: 14px 16px;
}

.ais-note span:not(.ais-icon) {
    color: #003ea8 !important;
    font-weight: 650 !important;
}

.ais-note .ais-icon {
    color: #0051d5 !important;
}

.ais-response-card {
    min-height: 590px;
}

.ais-empty {
    align-items: center;
    color: var(--ais-muted);
    display: flex;
    flex-direction: column;
    gap: 16px;
    justify-content: center;
    min-height: 170px;
    text-align: center;
}

.ais-empty .ais-icon {
    align-items: center;
    background: var(--ais-surface-low);
    border-radius: 999px;
    color: var(--ais-border-strong);
    display: inline-flex;
    font-size: 42px;
    height: 88px;
    justify-content: center;
    width: 88px;
}

.ais-output-stack {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.ais-output-stack .gradio-textbox textarea {
    background: var(--ais-surface-low) !important;
    border: 0 !important;
    color: var(--ais-text) !important;
    font-size: 16px !important;
    line-height: 24px !important;
}

.ais-transcript textarea {
    color: var(--ais-muted) !important;
    font-style: italic;
}

.ais-audio {
    border-top: 1px solid var(--ais-border);
    padding-top: 18px;
}

.ais-footer {
    align-items: center;
    background: var(--ais-surface-low);
    border: 1px solid var(--ais-border);
    border-radius: 16px;
    display: flex;
    justify-content: space-between;
    margin-top: 32px;
    padding: 16px 20px;
}

.ais-footer strong {
    color: var(--ais-text);
}

.ais-card .wrap,
.ais-card .block,
.ais-card .form,
.ais-card .gradio-container,
.ais-card .gradio-row {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

.ais-card .gradio-audio,
.ais-card .gradio-image,
.ais-card .gradio-video,
.ais-card .gradio-textbox {
    background: transparent !important;
    border: 0 !important;
    color: var(--ais-text) !important;
}

.ais-card .gradio-audio > div,
.ais-card .gradio-image > div,
.ais-card .gradio-video > div,
.ais-card .gradio-textbox > div {
    background: var(--ais-surface-low) !important;
    border: 1px solid var(--ais-border) !important;
    border-radius: 12px !important;
    color: var(--ais-text) !important;
}

.ais-card .gradio-audio [class*="container"],
.ais-card .gradio-image [class*="container"],
.ais-card .gradio-video [class*="container"],
.ais-card .gradio-textbox [class*="container"],
.ais-card .gradio-audio [class*="wrap"],
.ais-card .gradio-image [class*="wrap"],
.ais-card .gradio-video [class*="wrap"],
.ais-card .gradio-textbox [class*="wrap"] {
    background: var(--ais-surface-low) !important;
    border-color: var(--ais-border) !important;
    color: var(--ais-text) !important;
}

.ais-card .gradio-audio button,
.ais-card .gradio-image button,
.ais-card .gradio-video button,
.ais-card .gradio-textbox button {
    color: var(--ais-primary) !important;
}

.ais-card [data-testid="block-label"],
.ais-card div[class*="block-label"],
.ais-card label[class*="container"] {
    background: var(--ais-surface) !important;
    border-color: var(--ais-border) !important;
    color: var(--ais-muted) !important;
}

.ais-card [data-testid="block-label"] *,
.ais-card div[class*="block-label"] *,
.ais-card label[class*="container"] * {
    color: var(--ais-muted) !important;
}

.ais-card label span,
.ais-output-stack label span {
    color: var(--ais-muted) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

.ais-card input,
.ais-card textarea,
.ais-card select,
.ais-card .upload-container,
.ais-card .file-preview,
.ais-card .input-container,
.ais-card .dropzone,
.ais-card .empty,
.ais-card .icon-wrap,
.ais-card video,
.ais-card img {
    background: var(--ais-surface-low) !important;
    border-color: var(--ais-border) !important;
    color: var(--ais-text) !important;
    border-radius: 12px !important;
}

.ais-card input:disabled,
.ais-card textarea:disabled,
.ais-card [aria-disabled="true"],
.ais-card .disabled {
    background: var(--ais-surface-low) !important;
    color: var(--ais-text) !important;
    opacity: 1 !important;
    -webkit-text-fill-color: var(--ais-text) !important;
}

.ais-card .upload-container,
.ais-card .dropzone {
    min-height: 220px !important;
}

.ais-card .gradio-audio .upload-container,
.ais-card .gradio-audio .dropzone {
    min-height: 120px !important;
}

.ais-media-row .gradio-image,
.ais-media-row .gradio-video,
.ais-media-row .gradio-image > div,
.ais-media-row .gradio-video > div,
.ais-media-row .gradio-image [class*="container"],
.ais-media-row .gradio-video [class*="container"],
.ais-media-row .gradio-image [class*="wrap"],
.ais-media-row .gradio-video [class*="wrap"] {
    min-height: 280px !important;
    overflow: visible !important;
}

.ais-media-row .gradio-image .upload-container,
.ais-media-row .gradio-video .upload-container,
.ais-media-row .gradio-image .dropzone,
.ais-media-row .gradio-video .dropzone {
    height: 210px !important;
    min-height: 210px !important;
}

.ais-media-row .gradio-image button,
.ais-media-row .gradio-video button {
    min-height: 36px !important;
}

.ais-card .upload-container *,
.ais-card .file-preview *,
.ais-card .input-container *,
.ais-card .dropzone *,
.ais-card .empty * {
    color: var(--ais-text) !important;
}

.ais-card ::placeholder {
    color: var(--ais-border-strong) !important;
}

@media (max-width: 900px) {
    .ais-shell {
        padding: 20px;
    }

    .ais-topbar,
    .ais-footer {
        align-items: flex-start;
        flex-direction: column;
        gap: 14px;
    }

    .ais-grid,
    .ais-media-row {
        grid-template-columns: 1fr;
    }

    .ais-section-title h2 {
        font-size: 22px;
        line-height: 30px;
    }
}
"""


def process_inputs(audio_filepath, image_filepath, video_filepath):
    if not audio_filepath:
        raise gr.Error("Please record or upload your voice description first.")

    if not image_filepath and not video_filepath:
        raise gr.Error("Please upload a skin image or video before analysis.")

    try:
        patient_text = transcribe_patient_voice(audio_filepath)
        doctor_text = brain_of_the_doctor(
            patient_text=patient_text,
            image_filepath=image_filepath,
            video_filepath=video_filepath,
        )
        doctor_audio = convert_text_to_doctor_audio(doctor_text)

        return patient_text, doctor_text, str(doctor_audio)

    except (ValueError, IOError, OSError) as e:
        raise gr.Error(str(e))
    except Exception as e:
        raise gr.Error(f"An unexpected error occurred: {str(e)}")


with gr.Blocks(title=APP_TITLE) as iface:
    with gr.Column(elem_classes="ais-shell"):
        gr.HTML(
            """
            <header class="ais-topbar">
                <div class="ais-brand">
                    <h1>AI Skin Specialist</h1>
                    <p>VOICE, IMAGE, AND VIDEO BASED SKIN CONSULTATION ASSISTANT</p>
                </div>
                <div class="ais-security">
                    <span class="ais-icon">security</span>
                    <span>Privacy-first consultation</span>
                </div>
            </header>
            """
        )

        with gr.Row(elem_classes="ais-grid"):
            with gr.Column(scale=5):
                gr.HTML(
                    """
                    <div class="ais-section-title">
                        <span class="ais-icon">clinical_notes</span>
                        <h2>Patient Input</h2>
                    </div>
                    """
                )

                with gr.Column(elem_classes="ais-card ais-input-card"):
                    gr.HTML('<span class="ais-field-label">Describe your skin concern</span>')
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="Patient Voice",
                    )

                    with gr.Row(elem_classes="ais-media-row"):
                        image_input = gr.Image(
                            type="filepath",
                            label="Skin Image",
                            height=280,
                        )
                        video_input = gr.Video(label="Skin Video", height=280)

                    with gr.Column(elem_classes="ais-submit-wrap"):
                        analyze_button = gr.Button(
                            "Analyze Concern",
                            variant="primary",
                            size="lg",
                        )

                    gr.HTML(
                        """
                        <div class="ais-note">
                            <span class="ais-icon">info</span>
                            <span>For better assessment, include a short video showing the affected area from multiple angles and under good lighting.</span>
                        </div>
                        """
                    )

            with gr.Column(scale=7):
                gr.HTML(
                    """
                    <div class="ais-section-title">
                        <span class="ais-icon">smart_toy</span>
                        <h2>Doctor Response</h2>
                    </div>
                    """
                )

                with gr.Column(elem_classes="ais-card ais-response-card"):
                    gr.HTML(
                        """
                        <div class="ais-empty">
                            <span class="ais-icon">pending_actions</span>
                            <div>
                                <strong>Ready for Analysis</strong>
                                <p class="ais-panel-copy">Your consultation summary, transcript, and guidance will appear below after analysis.</p>
                            </div>
                        </div>
                        """
                    )

                    with gr.Column(elem_classes="ais-output-stack"):
                        transcript_output = gr.Textbox(
                            label="Your Speech Transcript",
                            lines=4,
                            interactive=False,
                            elem_classes="ais-transcript",
                        )
                        response_output = gr.Textbox(
                            label="Doctor's Guidance",
                            lines=9,
                            interactive=False,
                        )
                        audio_output = gr.Audio(
                            label="Doctor Voice Response",
                            type="filepath",
                            autoplay=True,
                            elem_classes="ais-audio",
                        )

                gr.HTML(
                    """
                    <div class="ais-security" style="justify-content:center; margin-top:16px;">
                        <span class="ais-icon">verified</span>
                        <span>AI guidance is informational and not a medical diagnosis</span>
                    </div>
                    """
                )

        gr.HTML(
            """
            <footer class="ais-footer">
                <div><strong>AI Skin Specialist</strong><br/>Consult a licensed dermatologist for urgent or serious symptoms.</div>
                <div>Privacy Policy · Terms of Service · Medical Disclaimer</div>
            </footer>
            """
        )

    analyze_button.click(
        fn=process_inputs,
        inputs=[audio_input, image_input, video_input],
        outputs=[transcript_output, response_output, audio_output],
    )


if __name__ == "__main__":
    iface.launch(debug=GRADIO_DEBUG, css=CSS, theme=gr.themes.Base())
