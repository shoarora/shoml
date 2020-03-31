import os

from pytorch_lightning import Callback


class PolyaxonGCSCheckpointCallback(Callback):
    def __init__(self):
        self.logged_artifact_paths = []

    def on_validation_end(self, trainer, pl_module):
        # only run on main process
        if trainer.proc_rank != 0:
            return

        experiment = pl_module.logger.experiment

        save_dir = trainer.checkpoint_callback.dirpath
        local_checkpoints = os.listdir(save_dir)

        for path in local_checkpoints:
            filepath = os.path.join(save_dir, path)
            if filepath not in self.logged_artifact_paths:
                experiment.log_artifact(filepath)
                self.logged_artifact_paths.append(filepath)
