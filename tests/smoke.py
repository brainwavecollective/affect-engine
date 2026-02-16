import asyncio
import time

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)


from affect_engine import AffectEngine, AffectConfig


async def run_smoke_test():
    config = AffectConfig(
        enable_anchor=False,
        debug=True,
    )

    engine = AffectEngine(config)

    updates = []

    def subscriber(vibe):
        updates.append((time.time(), vibe))

    engine.subscribe(subscriber)

    # Start engine (loads models)
    await engine.start()

    # Let it tick a bit
    await asyncio.sleep(0.5)

    # Send text
    result = await engine.process_text(
        "I am absolutely thrilled to be here. This is incredible!"
    )

    assert "vibe" in result
    assert len(result["vibe"]) == 5

    # Let decay loop run
    await asyncio.sleep(1.5)

    # Stop engine
    await engine.stop()

    # Assertions
    assert len(updates) > 5, "Engine did not tick properly"
    assert any(v[1][0] > 0.5 for v in updates), "Valence never increased"

    print("SMOKE TEST PASSED")


if __name__ == "__main__":
    asyncio.run(run_smoke_test())
