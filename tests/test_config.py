from audiototext.config import parse_args


def test_parse_defaults():
    config = parse_args(["sample.mp3"])
    assert config.audio_files[0].name == "sample.mp3"
    assert config.task == "transcribe"
    assert config.model == "small"
    assert config.output_formats == ("txt", "vtt", "srt", "tsv", "json")


def test_parse_custom_formats():
    config = parse_args(["sample.wav", "--output-formats", "txt,srt"])
    assert config.output_formats == ("txt", "srt")
