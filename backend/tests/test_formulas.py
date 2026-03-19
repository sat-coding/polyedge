from app.core.formulas import expected_value, kelly_fraction, bayesian_update, log_return

def test_ev(): assert expected_value(0.4, 0.6) > 0

def test_kelly_non_negative(): assert kelly_fraction(0.7, 0.5) >= 0

def test_bayesian_clamp(): assert 0.01 <= bayesian_update(0.6, 0.8, 0.7) <= 0.99

def test_log_return(): assert log_return(100, 110) > 0
