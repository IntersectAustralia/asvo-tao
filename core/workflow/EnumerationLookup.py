class JobState:
    NewJob=0
    Queued=1
    Running=2
    Completed=3
    Error=4
    Paused=5
class CommandState:
    NewCommand=0    
    Completed=1
    Error=2
    
class JobType:
    Simple=0
    Complex=1
class EventType:
    Normal=0
    PBSEvent=1
    Error=999