#!/usr/bin/env python2.7

import requests
import json
import time
import sys
# Used with the ENV vars set within the Github Action.
import os

GITHUB_REPO=os.environ["GITHUB_REPOSITORY"]
GITHUB_TOKEN=os.environ["GITHUB_TOKEN"]
GITHUB_SHA=os.environ["GITHUB_SHA"]

with open(os.environ["GITHUB_EVENT_PATH"]) as json_file:
    data = json.load(json_file)
    GITHUB_PULL_NUMBER = data['number']

BASE_GITHUB_URI="https://api.github.com/"
API_VERSION="v3"
# We require the antiope-preview for the check-runs preview.
API_HEADER={
    "Accept": "application/vnd.github.{}+json".format(API_VERSION),
    "Accept": "application/vnd.github.antiope-preview+json",
    "Authorization": "token {}".format(GITHUB_TOKEN)
}


def get_chuck_norris_gif(status):
    """
        Return a gif link based on good or bad build status
    """
    return "![](https://raw.githubusercontent.com/GregSharpe1/chuck-norris-action/master/img/{}-chuck/1.gif)".format(status)


def get_remove_old_comment():
    """
        Remove the chuck if exists
    """

    COMMENTS_GITHUB_URI = BASE_GITHUB_URI + "repos/{}/issues/comments".format(GITHUB_REPO)
    github_comments = requests.get(COMMENTS_GITHUB_URI, headers=API_HEADER).json()

    for comment in github_comments:
        # Loop through every commment if a comment exists with chuck norris .gif remove it.
        if "chuck-norris-action" and ".gif" in comment["body"]:
            # We've found a chuck norris . gif related comment
            # Let's remove it as assuming it's been posted by this action before.
            print("Removing comment: {}".format(comment["id"]))
            DELETE_COMMENT_URL = COMMENTS_GITHUB_URI + "/{}".format(comment["id"])
            print DELETE_COMMENT_URL
            response = requests.delete(DELETE_COMMENT_URL, headers=API_HEADER)

def set_github_comment(status):
    """
        Post the chuck status on PR
    """
    COMMENTS_GITHUB_URI = BASE_GITHUB_URI + "repos/{}/issues/{}/comments".format(GITHUB_REPO, GITHUB_PULL_NUMBER)

    payload = {
        "body": get_chuck_norris_gif(status)
    }
    requests.post(COMMENTS_GITHUB_URI, headers=API_HEADER, data=json.dumps(payload)).json()


def get_pull_request_status():
    """
        Return the status of the pull request in question.
    """
    STATUS_ENDPOINT = BASE_GITHUB_URI + "repos/{}/commits/{}/check-runs".format(GITHUB_REPO, GITHUB_SHA)
    status = requests.get(STATUS_ENDPOINT, headers=API_HEADER).json()

    in_progress = 0
    # To check the status I need to extract the follow values
    for state in status["check_runs"]:
        if os.environ["GITHUB_ACTION"] == state["name"]:
            print "LOG: Github action matches, we're good too go.."

        if state["status"] == "in_progress":
            print "LOG: Build status still in progress..."
            in_progress = 1

        # If the status is complete and fails, post bad commment
        if state["status"] == "completed" and state["conclusion"] == "failure":
            print "LOG: Build status returning failed, posting bad chuck norris..."

            # First let's remove the old comments
            get_remove_old_comment()
            # Post the "bad" chuck norris gif
            set_github_comment("bad")

            sys.exit(0)

        elif state["status"] == "completed" and state["conclusion"] == "success":
            print "LOG: Build status returned success, posting good chuck norris..."

            # First let's remove the old comments
            get_remove_old_comment()
            # Post the "bad" chuck norris gif
            set_github_comment("good")

            sys.exit(0)

    if in_progress == 1:
        print "LOG: Build still in progress, re-running the get pull request status function."

        time.sleep(2)
        get_pull_request_status()

    return


def main():
    """
        Get the most recent build status -> return chuck norris image
        clear any comments
        post chuck status
    """

    get_pull_request_status()


# call the main script everrrrrrry time
if __name__ == "__main__":
    main()