import typing

from datasources import isearchd_provider
from domain.config import Config
from presentation import cli_executor_impl
from domain.executor import CLIExecutor


def Init(cfg: Config) -> CLIExecutor:
    provider = isearchd_provider.SearchProviderImpl(cfg.socket_path)
    executor = cli_executor_impl.CLIExecutorImpl(cfg, provider)
    return executor
