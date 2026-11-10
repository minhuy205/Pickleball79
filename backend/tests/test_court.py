import numpy as np

from tracking.court import COURT_LENGTH_M, COURT_WIDTH_M, CourtCalibration


def make_calib():
    # Hình thang giả lập góc nhìn từ phía sau sân
    return CourtCalibration(np.array([[200, 700], [1000, 700], [850, 200], [350, 200]], np.float32))


def test_corners_map_to_court_corners():
    c = make_calib()
    out = c.to_court(c.image_points)
    expected = np.array([[0, 0], [COURT_WIDTH_M, 0], [COURT_WIDTH_M, COURT_LENGTH_M], [0, COURT_LENGTH_M]])
    assert np.allclose(out, expected, atol=1e-3)


def test_roundtrip():
    c = make_calib()
    pts = np.array([[3.0, 5.0], [1.0, 10.0]], np.float32)
    assert np.allclose(c.to_court(c.to_image(pts)), pts, atol=1e-3)


def test_save_load(tmp_path):
    c = make_calib()
    c.save(tmp_path / "c.json")
    c2 = CourtCalibration.load(tmp_path / "c.json")
    assert np.allclose(c.H, c2.H, atol=1e-6)
