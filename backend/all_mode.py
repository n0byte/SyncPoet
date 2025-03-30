def all_mode():
    print("Processing all mode...")

    # Importe hier durchführen, um Circular Import zu vermeiden
    from mode import c2m_mode, m2c_mode

    # First C2M
    c2m_mode()

    # Second M2C
    m2c_mode()

    print("All mode successfuly finished.")
