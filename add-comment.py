#!/usr/bin/env python2.7

import requests
import json

# Used with the ENV vars set within the Github Action.
import os

GITHUB_REPO=os.environ["GITHUB_REPOSITORY"]
GITHUB_TOKEN=os.environ["GITHUB_TOKEN"]


with open(os.environ["GITHUB_EVENT_PATH"]) as json_file:
    data = json.load(json_file)
    GITHUB_PULL_NUMBER = data['number']

BASE_GITHUB_URI="https://api.github.com/"
API_VERSION="v3"
API_HEADER={
    "Accept": "application/json",
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
        print comment["body"]
        print comment["id"]
        if "1.gif" in comment["body"]:
            # We've found a chuck norris . gif related comment
            # Let's remove it as assuming it's been posted by this action before.
            print("Removing comment: {}".format(comment["id"]))
            DELETE_COMMENT_URL = COMMENTS_GITHUB_URI + "/{}".format(comment["id"])
            print DELETE_COMMENT_URL
            response = requests.delete(DELETE_COMMENT_URL, headers=API_HEADER)

    return response


def set_github_comment(status):
    """
        Post the chuck status on PR
    """
    COMMENTS_GITHUB_URI = BASE_GITHUB_URI + "repos/{}/issues/{}/comments".format(GITHUB_REPO, GITHUB_PULL_NUMBER)

    payload = {
        "body": get_chuck_norris_gif(status)
    }
    response = requests.post(COMMENTS_GITHUB_URI, headers=API_HEADER, data=json.dumps(payload))
    return response.json()


def main():
    """
        Get the most recent build status -> return chuck norris image
        clear any comments
        post chuck status
    """

    get_remove_old_comment()

    set_github_comment("good")

    print "Sent chuck chuck"

# call the main script everrrrrrry time
if __name__ == "__main__":
    main()