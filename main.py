import argparse
from file_utils import check_file_exists, identify_file_type
from image_analyzer import analyze_image
from audio_analyzer import analyze_audio
from video_analyzer import analyze_video
from report_generator import generate_report
from image_enhancer import enhance_image
from voice_cloner import clone_and_generate
from speech_to_speech import convert_speech_to_speech

def main():
    parser = argparse.ArgumentParser(description="Multimedia Analyzer")
    parser.add_argument("file_path", help="Path to media file")
    parser.add_argument("--enhance", action="store_true", help="Enhance image files")
    parser.add_argument("--clone-voice", type=str, help="Text to generate using the audio file as a voice clone", dest="clone_voice")
    parser.add_argument("--speech-to-speech", action="store_true", help="Convert audio file using Speech-to-Speech API", dest="sts")
    
    args = parser.parse_args()
    file_path = args.file_path
    
    if not check_file_exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    file_type = identify_file_type(file_path)
    
    report_data = {
        "File Type Identified": file_type
    }
    
    if file_type == "IMAGE":
        report_data.update(analyze_image(file_path))
        if args.enhance:
            output = enhance_image(file_path, brightness=1.2, contrast=1.2, color=1.2, sharpness=1.5, denoise=True)
            print(f"Enhanced image saved to: {output}")
            report_data["Enhanced Image Path"] = output
    elif file_type == "AUDIO":
        report_data.update(analyze_audio(file_path))
        if args.clone_voice:
            try:
                result = clone_and_generate(file_path, args.clone_voice)
                print(f"Cloned voice saved to: {result['output_file']}")
                report_data["Cloned Voice Path"] = result["output_file"]
            except Exception as e:
                print(f"Error cloning voice: {e}")
                report_data["Cloned Voice Error"] = str(e)
        if args.sts:
            try:
                print("Running Speech-to-Speech conversion...")
                out_path = convert_speech_to_speech(file_path)
                print(f"Speech-to-Speech audio saved to: {out_path}")
                report_data["Speech-to-Speech Path"] = out_path
            except Exception as e:
                print(f"Error converting speech: {e}")
                report_data["Speech-to-Speech Error"] = str(e)
    elif file_type == "VIDEO":
        report_data.update(analyze_video(file_path))
    else:
        print("Error: Unsupported file format.")
        return

    generate_report(report_data, output_dir="reports")

if __name__ == "__main__":
    main()
