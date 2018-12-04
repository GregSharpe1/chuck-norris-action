FROM python:3.6-alpine

LABEL "com.github.actions.name"="Chuck Norris"
LABEL "com.github.actions.description"="Displays a chuck norris gif based on PR state"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="blue"

RUN pip install -r requirements

COPY add-comment.py /usr/local/bin/add-comment

CMD ["add-comment"]
