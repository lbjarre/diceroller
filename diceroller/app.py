from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from diceroller.dice import DiceRoll

app = FastAPI()


@app.get("/distribution")
async def distribution(roll: str):
    if (diceroll := DiceRoll.parse(roll)) is None:
        return JSONResponse(
            content={"error": f"Could not parse dice {roll}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return {outcome: diceroll.prob(outcome) for outcome in diceroll.possible_outcomes()}


@app.get("/head")
async def head(roll: str, outcome: int):
    if (diceroll := DiceRoll.parse(roll)) is None:
        return JSONResponse(
            content={"error": f"Could not parse dice {roll}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return diceroll.prob_leq(outcome)


@app.get("/tail")
async def tail(roll: str, outcome: int):
    if (diceroll := DiceRoll.parse(roll)) is None:
        return JSONResponse(
            content={"error": f"Could not parse dice {roll}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return diceroll.prob_geq(outcome)
