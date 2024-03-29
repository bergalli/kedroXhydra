"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import node, pipeline

from .nodes import predict, report_accuracy, train_model


def create_pipeline(**kwargs):
    return pipeline(
        [
            node(
                train_model,
                [
                    "example_train_x",
                    "example_train_y",
                    "params:num_iter",
                    "params:learning_rate",
                ],
                "example_model",
                name="train",
            ),
            node(
                predict,
                dict(model="example_model", test_x="example_test_x"),
                "example_predictions",
                name="predict",
            ),
            node(
                report_accuracy,
                ["example_predictions", "example_test_y"],
                None,
                name="report",
            ),
        ]
    )
