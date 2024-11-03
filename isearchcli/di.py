"""Module with dependency injection utilities."""
from datasources import isearchd_provider
from domain.config import Config
from presentation import cli_executor_impl
from domain.interfaces.executor import CLIExecutor


def Init(cfg: Config) -> CLIExecutor:
    """Injects all dependencies."""
    provider = isearchd_provider.DaemonProviderImpl(cfg.socket_path)
    executor = cli_executor_impl.CLIExecutorImpl(cfg, provider)
    return executor
