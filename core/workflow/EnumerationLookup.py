class JobState:
    NewJob=0
    SubmittedToPBX=1
    Running=2
    Completed=3

class EventType:
    Normal=0
    PBSEvent=1
    Error=999