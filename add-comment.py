#!/usr/bin/env python2.7

import requests
import json

# Used with the ENV vars set within the Github Action.
import os

GITHUB_REPO=os.environ["GITHUB_REPO"]
GITHUB_PULL_NUMBER=os.environ["GITHUB_PULL_NUMBER"]
GITHUB_TOKEN=os.environ["GITHUB_TOKEN"]

BASE_GITHUB_URI="https://api.github.com/"
API_VERSION="v3"
API_HEADER={
    "Accept": "application/json",
    "Authorization": "token {}".format(GITHUB_TOKEN)
}

def get_chuck_norris_gif(status):
    """
        Return a gif link based on good or bad input
    """

    if status == "good":
        # Run a random function to return a link within the repos img/good-chuck dir
        CHUCK_GIT_URL = "https://raw.githubusercontent.com/GregSharpe1/chuck-norris-action/master/img/good-chuck/1.gif"

    elif status == "bad":
        # Run the return random link function with bad being pass into it.
        CHUCK_GIT_URL = "https://raw.githubusercontent.com/GregSharpe1/chuck-norris-action/master/img/bad-chuck/1.gif"

    return CHUCK_GIT_URL

def get_remove_old_comment():
    """
        Remove the chuck if exists
    """

    COMMENTS_GITHUB_URI = BASE_GITHUB_URI + "repos/GregSharpe1/{}/issues/{}/comments".format(GITHUB_REPO, GITHUB_PULL_NUMBER)
    github_comments = requests.get(COMMENTS_GITHUB_URI, headers=API_HEADER).json()

    # print github_comments

    for comment in github_comments:
        # Loop through every commment if a comment exists with chuck norris .gif remove it.
        print comment["body"]
        print comment["id"]
        if "thumb_up.jpg" in comment["body"]:
            # We've found a chuck norris . gif related comment
            # Let's remove it as assuming it's been posted by this action before.
            print("Removing comment: {}".format(comment["id"]))
            DELETE_COMMENT_URL = COMMENTS_GITHUB_URI + "/{}".format(comment["id"])
            print DELETE_COMMENT_URL
            response = requests.delete(DELETE_COMMENT_URL, headers=API_HEADER)

    return response.json()

def set_github_comment(status):
    """
        Post the chuck status on PR
    """
    COMMENTS_GITHUB_URI = BASE_GITHUB_URI + "repos/GregSharpe1/{}/issues/{}/comments".format(GITHUB_REPO, GITHUB_PULL_NUMBER)

    payload = {
        "body": get_chuck_norris_gif(status)
    }
    response = requests.post(COMMENTS_GITHUB_URI, headers=API_HEADER, data=json.dumps(payload))
    return response.json()