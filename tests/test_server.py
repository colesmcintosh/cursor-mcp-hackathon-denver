import asyncio

import pytest

import server


def test_app_metadata_matches_constants():
    assert getattr(server.app, "name", None) == server.APP_NAME
    assert getattr(server.app, "instructions", None) == server.APP_DESCRIPTION


def test_hackathon_overview_returns_expected_resource():
    resource = server.hackathon_overview
    assert resource.name == "Hackathon Overview"
    assert resource.mime_type == "text/markdown"
    assert asyncio.run(resource.read()) == server.HACKATHON_MARKDOWN


@pytest.mark.parametrize("expected_segment", [
    "## Overview",
    "## Goals",
    "## Architecture at a Glance",
    "## Getting Started",
    "## Unique Project Ideas",
    "## Rules and Format",
    "## Resources",
    "## Let’s Build",
])
def test_hackathon_markdown_contains_key_sections(expected_segment):
    assert expected_segment in server.HACKATHON_MARKDOWN


def test_fastmcp_python_prompt_has_two_messages():
    prompt = server.fastmcp_python_prompt
    messages = asyncio.run(prompt.render())
    assert len(messages) == 2

    system_message, user_message = messages
    assert system_message.role == "assistant"
    assert "FastMCP engineer" in system_message.content.text

    assert user_message.role == "user"
    assert user_message.content.text == server.PROMPT_TEMPLATE


def test_prompt_template_guidance():
    template = server.PROMPT_TEMPLATE
    for keyword in ("fastmcp", "@app.resource", "structured results"):
        assert keyword in template
