import functools
import logging
import random
import sys
import time

import click

from .distinct import CountDistinct


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def log_timing(fn):
    @functools.wraps(fn)
    def _inner(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        elapsed = time.time() - start

        logger.info(
            f"Found {result} distinct elements in "
            f"{elapsed:.2f} seconds using {fn.__name__} algorithm"
        )

    return _inner


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

    # Generate test data
    # Set random seed so data remains unchanged across runs
    r = random.Random(0)
    ctx.obj["data"] = [str(r.randrange(100000)) for _ in range(100000)]


@cli.command()
@click.pass_context
@log_timing
def naive(ctx):
    ctx.ensure_object(dict)
    return list(CountDistinct.naive(ctx.obj["data"]))[-1]


@cli.command()
@click.option("--capacity", default=100, type=click.INT)
@click.pass_context
@log_timing
def cvm(ctx, capacity: int):
    ctx.ensure_object(dict)
    return list(CountDistinct.cvm(ctx.obj["data"], capacity=capacity))[-1]
