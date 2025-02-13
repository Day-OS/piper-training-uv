

    def lr_scheduler_step(self, scheduler, metric, optimizer_idx, *args, **kwargs):
        scheduler.step()