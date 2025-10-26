import os
import subprocess


def test_cli_command():
    """Интеграционный тест CLI команды"""
    file1 = os.path.join("tests", "fixtures", "file1.json")
    file2 = os.path.join("tests", "fixtures", "file2.json")

    result = subprocess.run(
        ["python", "-m", "gendiff", file1, file2],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    assert result.returncode == 0
    assert "common" in result.stdout
    assert "follow" in result.stdout


def test_cli_command_with_format():
    """Интеграционный тест CLI команды с форматом"""
    file1 = os.path.join("tests", "fixtures", "file1.json")
    file2 = os.path.join("tests", "fixtures", "file2.json")

    result = subprocess.run(
        ["python", "-m", "gendiff", file1, file2, "--format", "stylish"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    assert result.returncode == 0
    assert "common" in result.stdout


def test_cli_command_help():
    """Интеграционный тест CLI помощи"""
    result = subprocess.run(
        ["python", "-m", "gendiff", "--help"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    assert result.returncode == 0
    assert "Compares two configuration files" in result.stdout


def test_cli_command_version():
    """Интеграционный тест CLI версии"""
    result = subprocess.run(
        ["python", "-m", "gendiff", "--version"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    assert result.returncode == 0
    assert "1.0" in result.stdout


def test_cli_command_nonexistent_file():
    """Интеграционный тест CLI с несуществующим файлом"""
    result = subprocess.run(
        ["python", "-m", "gendiff", "nonexistent1.json", "nonexistent2.json"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )

    assert "not found" in result.stderr
    assert result.returncode == 1
