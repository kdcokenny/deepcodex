from pathlib import Path

import yaml
from pier.agents.factory import AgentFactory
from pier.models.job.config import JobConfig

from deepcodex_bench.agents import LazyCodexStartWork


def test_start_work_instruction_when_task_body_is_plain_text(tmp_path: Path) -> None:
    agent = LazyCodexStartWork(logs_dir=tmp_path, model_name="openai/gpt-5.5")

    instruction = agent._start_work_instruction("Fix the failing test.")

    assert instruction == "$start-work\n\nFix the failing test."


def test_lazycodex_install_command_when_default_package_is_used(tmp_path: Path) -> None:
    agent = LazyCodexStartWork(logs_dir=tmp_path, model_name="openai/gpt-5.5")

    command = agent._lazycodex_install_command()
    lazycodex_args = "install --no-tui --codex-autonomous --skip-auth"

    assert f"bunx --yes lazycodex-ai@latest {lazycodex_args}" in command
    assert f"npx --yes lazycodex-ai@latest {lazycodex_args}" in command
    assert 'CODEX_HOME="${CODEX_HOME:?CODEX_HOME must be set}"' in command


def test_lazycodex_install_command_when_package_is_overridden(tmp_path: Path) -> None:
    agent = LazyCodexStartWork(
        logs_dir=tmp_path,
        model_name="openai/gpt-5.5",
        lazycodex_package="lazycodex-ai@0.1.0",
    )

    command = agent._lazycodex_install_command()

    assert "lazycodex-ai@0.1.0 install --no-tui --codex-autonomous --skip-auth" in command


def test_configs_allow_chatgpt_account_auth_egress(tmp_path: Path) -> None:
    for config_path in ["configs/codex-base.yaml", "configs/lazycodex-start-work.yaml"]:
        data = yaml.safe_load(Path(config_path).read_text())
        config = JobConfig.model_validate(data)
        agent = AgentFactory.create_agent_from_config(config.agents[0], logs_dir=tmp_path)

        allowlist = agent.network_allowlist()

        assert "api.openai.com" in allowlist.domains
        assert "chatgpt.com" in allowlist.domains
