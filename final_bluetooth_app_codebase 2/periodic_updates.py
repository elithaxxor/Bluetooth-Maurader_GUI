import asyncio

async def periodic_updates(client):
    """
    Periodically simulate data changes for battery level, heart rate, etc.
    The updates are triggered every 5 seconds.
    """
    while True:
        # Simulate battery level and heart rate
        simulate_battery_level(client)
        simulate_heart_rate(client)

        # Wait for 5 seconds before updating again
        await asyncio.sleep(5)
