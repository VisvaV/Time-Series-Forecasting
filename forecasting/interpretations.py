def interpret_acf_pacf(acf_values, pacf_values):
    """Interpret ACF and PACF values correctly."""

    if isinstance(acf_values, (int, float)):
        acf_values = [acf_values]
    if isinstance(pacf_values, (int, float)):
        pacf_values = [pacf_values]

    if len(acf_values) < 5:
        acf_values += [0] * (5 - len(acf_values))
    if len(pacf_values) < 5:
        pacf_values += [0] * (5 - len(pacf_values))

    return {
        "Strong Positive ACF": any(v > 0.5 for v in acf_values[:5]),
        "Strong Negative ACF": any(v < -0.5 for v in acf_values[:5]),
        "Strong Positive PACF": any(v > 0.5 for v in pacf_values[:5]),
        "Strong Negative PACF": any(v < -0.5 for v in pacf_values[:5]),
    }
