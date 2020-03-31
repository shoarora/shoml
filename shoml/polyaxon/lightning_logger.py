import os

from polyaxon_client.tracking import Experiment
from pytorch_lightning.loggers import (LightningLoggerBase, TensorBoardLogger,
                                       rank_zero_only)
from torch import is_tensor


class PolyaxonLogger(LightningLoggerBase):
    def __init__(self, use_tensorboard=True):
        self._experiment = Experiment()

        self.use_tensorboard = use_tensorboard
        if use_tensorboard:
            save_dir = os.path.join(self._experiment.get_outputs_path(), "tensorboard")
            self.tensorboard = TensorBoardLogger(save_dir)

        self._name = self._experiment.project_name
        self._version = self._experiment.experiment_id
        self._experiment = None

    @property
    def experiment(self):
        if self._experiment is None:
            self._experiment = Experiment()
        return self._experiment

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @rank_zero_only
    def log_hyperparams(self, params):
        # polyaxon tracking currently doesn't support this
        # polyaxon is responsible for launching experiments,
        # so it has access to the param declarations there.
        if self.use_tensorboard:
            self.tensorboard.log_hyperparams(params)

    @rank_zero_only
    def log_metrics(self, metrics, step):
        for key, val in metrics.items():
            if is_tensor(val):
                metrics[key] = val.cpu().detach()
        self.experiment.log_metrics(step=step, **metrics)
        if self.use_tensorboard:
            self.tensorboard.log_metrics(metrics, step)

    def save(self):
        if self.use_tensorboard:
            self.tensorboard.save()

    def finalize(self, status):
        if self.use_tensorboard:
            self.tensorboard.finalize(status)
