# -------------------------------------------------------------------------
# Copyright (c) Thomas Waldinger. All rights reserved.
# Licensed under the Apache License, Version 2.0. See
# License.txt in the project root for license
# information.
# ---------------

"""
Job
The Job resource tracks jobs submitted to the P5 server. Information about each
of the submitted jobs is held indefinitely and can be queried by the user at
any time. Job resources are generated automatically, for instance by the submit
methods of the ArchiveSelection resource.
"""
from awp5.base.connection import P5Resource, exec_nsdchat
from awp5.base.helpers import resourcelist, onereturnvalue

module_name = "Job"


def names(as_object=False, p5_connection=None):
    """
    Syntax: Job names
    Description: Returns a list of all currently scheduled or running jobs
    Return Values:
    -On Success:    the names of currently scheduled or running jobs
                    the string "<empty>" if no jobs are scheduled
    """
    method_name = "names"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


def completed(lastdays=None, as_object=False, p5_connection=None):
    """
    Syntax: Job completed [<lastdays>]
    Description: Returns the names of all jobs completed by the system.
    If the optional  <lastdays> argument is not given, jobs completed today are
    returned.
    Otherwise, all completed jobs for the last <lastdays> days are returned.
    The <lastdays> argument is interpreted as a positive integer (the default
    is 0 meaning today).
    Return Values:
    -On Success:    the names of completed jobs or
                    the string "<empty>" if no jobs completed
                    in the given time.
    """
    method_name = "completed"
    result = exec_nsdchat([module_name, method_name, lastdays],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def completion(job_name, p5_connection=None):
    """
    Syntax: Job <name> completion
    Description: Returns the completion code of the completed job. The
    completion code can be one of:
        • success
        • exception
        • failure
    The success completion code means that the job has completed successfully
    in its entirety. It does not mean that all of the files have been archived
    and/or restored, though. For info about the particular file, use the
    protocol method.
    The exception completion code means that parts of the job have failed, but
    the job may have been partially executed successfully. This happens for
    parallel archive/restore operations where one of the job threads runs into
    an error, while others continue to run and finish successfully.
    The failure completion code means that the job has failed in its entirety
    and none of the files have been processed (archived/restored) correctly.
    Return Values:
    -On Success:    one of the completion codes
    """
    method_name = "completion"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


@onereturnvalue
def describe(job_name, p5_connection=None):
    """
    Syntax: Job <name> describe
    Description: Returns a (human readable) job description as shown in the P5
    job monitor.
    Return Values:
    -On Success:    the job description
    """
    method_name = "describe"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


def failed(lastdays=None, as_object=False, p5_connection=None):
    """
    Syntax: Job failed [<lastdays>]
    Description: Returns the names of all the jobs that failed to execute. If
    no optional argument <lastdays> is given, it returns jobs that failed
    today.
    Otherwise, all failed jobs for the last <lastdays> days are returned.
    The <lastdays> argument is interpreted as a positive integer (0 means
    today).
    Return Values:
    -On Success:    the names of failed jobs
                    the string "<empty>" if no jobs failed
    """
    method_name = "failed"
    result = exec_nsdchat([module_name, method_name, lastdays],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def inventory(job_name, outputfile, options=None, p5_connection=None):
    """
    Syntax: Job <name> inventory <output file> [<options>]
    Description: Outputs a list of the files saved by the Archive-Job <name>
    into a file.
    The <output file> must be in the form [client:]absolute_path whereby client
    is the name of the P5 client where to store the file and absolute_path is
    the complete path to the file to hold the output. The client part is
    optional and defaults to localhost:
    The inventory command fills in the passed file with lines containing
    records separated by a TAB. If no <options> are given, the output file will
    by default contain the index paths of all the files saved by the given job
    <name>, one record per line. Additional <options> represent the attributes
    that will be output for each file in a tab-separated format. These
    attributes may be system attributes or any user-defined meta-data fields.
    The supported system attributes are:

    ppath:
    volumes:

    size:
    handle:
    btime:
    mtime:
    ino:
    the physical path of the file on the filesystem
    a blank separated list of the volumes where the file is saved
    the size of the saved file
    the handle as required by the RestoreSelection
    the backup time of the file
    the file's modification time
    the inode number of the file

    The index path returned by the inventory command cannot be used to access
    files on the file system in general. There are special cases where this
    might be used for this purpose, but generally it is not supported. The idea
    behind this info is to have an overview or idea what is being stored in the
    index and not to consume it in some other fashion (i.e. address the files
    on the file system to post-process them).
    In cases where files are still expected to be in the file system at the
    place they were at the point of archiving (for example somebody wants to
    delete them or otherwise post-process them) the ppath attribute may be
    used, which, when given on the command line, will yield the physical path
    as-found on the client where the file resides. Note that not all index
    entries have corresponding physical paths. In such cases the value will
    be set to the string "<empty>".
    Return Values:
    -On Success:    the <client>:<output file>
    """
    method_name = "inventory"
    return exec_nsdchat([module_name, job_name, method_name, outputfile,
                        options], p5_connection)


@onereturnvalue
def label(job_name, p5_connection=None):
    """
    Syntax: Job <name> label
    Description: Returns the (human readable) job label.
    The following labels are returned:
    Archive, Backup, Synchronize and System.
    A Job label can be used in conjunction with the Job describe command to
    better display the job record in various list displays.
    Return Values:
    -On Success:    the job label
    """
    method_name = "label"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


def pending(as_object=False, p5_connection=None):
    """
    Syntax: Job pending
    Description: Returns the names of all the jobs waiting to be executed, i.e.
    jobs that are still in the queue waiting to be scheduled and jobs that are
    already scheduled but wait for the next free worker thread.
    Return Values:
    -On Success:    the names of currently waiting jobs
                    the string "<empty>" if no jobs are waiting
    """
    method_name = "pending"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def protocol(job_name, archiveentry=None, p5_connection=None):
    """
    Syntax: Job <name> protocol [<archiveentry>]
    Description: Returns a completion protocol of the completed job and/or of
    one of the archived and/or restored file(s) given by the optional
    <archiveentry> argument. The protocol contains human readable text.
    Return Values:
    -On Success:    the requested protocol
    """
    method_name = "protocol"
    return exec_nsdchat([module_name, job_name, method_name, archiveentry],
                        p5_connection)


@onereturnvalue
def report(job_name, p5_connection=None):
    """
    Syntax: Job <name> report
    Description: Returns a report of the currently running job. The report
    contains human readable text.
    Return Values:
    -On Success:    the report text
    """
    method_name = "report"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


@onereturnvalue
def resourcegroup(job_name, p5_connection=None):
    """
    Syntax: Job <name> resourcegroup
    Description: Returns the name of the resource group for which this job has
    been running.
    Return Values:
    -On Success:    the name of the resource group
                    (for example ArchivePlan, SyncPlan, etc.)
                    or the string "<empty>",
                    if no resource group is associated with the job
    """
    method_name = "resourcegroup"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


@onereturnvalue
def resourcename(job_name, p5_connection=None):
    """
    Syntax: Job <name> resourcename
    Description: Returns the name of the resource for which this job has been
    running
    Return Values:
    -On Success:    the name of the resource
                    (for example Default-Backup, Default-Archive)
                    or the string "<empty>",
                    if no resource group is associated with the job
    """
    method_name = "resourcename"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


def running(as_object=False, p5_connection=None):
    """
    Syntax: Job running
    Description: Returns the names of all currently running jobs.
    Return Values:
    -On Success:    the names of currently running jobs
                    the string "<empty>" if no jobs are running
    """
    method_name = "running"
    result = exec_nsdchat([module_name, method_name], p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def status(job_name, p5_connection=None):
    """
    Syntax: Job <name> status
    Description: Returns the status of the job. A job can have a number of
    internal statuses, depending on the stage of the archive and/or restore
    process. Currently, the following statuses are supported:
        • started   the job is starting (intermediate state)
        • stopped   the job is stopping (intermediate state)
        • unknown   the job is not known by the system
        • scheduled the job is in the queue waiting to be run
        • pending   an intermediate state during start,
                    the job is waiting to be accepted for start
                    by the queue manager
        • running   the job is running
        • canceled  the job is canceled by user
        • completed the job is completed
        • terminated        the job is terminated by a server shutdown
    Return Values:
    -On Success:    one of the supported statuses
    """
    method_name = "status"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


def warning(lastdays=None, as_object=False, p5_connection=None):
    """
    Syntax: Job warning [<lastdays>]
    Description: Returns names of all jobs with warnings. If no optional
    argument <lastdays> is given, it returns jobs with warnings from today.
    Otherwise, all jobs with warnings for the last <lastdays> days are
    returned.
    The <lastdays> argument is interpreted as a positive integer (0 = today).
    Return Values:
    -On Success:    the names of jobs with warnings
                    the string "<empty>" if no jobs ended with a warning
    """
    method_name = "warning"
    result = exec_nsdchat([module_name, method_name, lastdays],
                          p5_connection)
    if not as_object:
        return result
    else:
        return resourcelist(result, Job, p5_connection)


@onereturnvalue
def xmlticket(job_name, outputfile=None, p5_connection=None):
    """
    Syntax: Job <name> xmlticket [<outfilename>]
    Description: Returns the completion protocol of the completed job.
    The protocol contains human readable text embedded in generic XML sections.
    If the optional <outfilename> argument is given, the output of the command
    is rerouted to the given file.
    Return Values:
    -On Success:    the requested protocol
    """
    method_name = "xmlticket"
    return exec_nsdchat([module_name, job_name, method_name,
                        outputfile], p5_connection)


@onereturnvalue
def cancel(job_name, p5_connection=None):
    """
    Syntax: Job <name> cancel
    Description: Cancels the running job. Only jobs that have the running
    status can be canceled. An attempt to cancel a job with a different status
    will result in an error.
    Return Values:
    -On Success:    the string "1" if the job is canceled
                    the string "0" if the job could not be canceled
                    for whatever reason
    """
    method_name = "cancel"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


@onereturnvalue
def runat(job_name, p5_connection=None):
    """
    Syntax: Job <name> runat
    Description: Returns the time in seconds (Posix time) when the job was
    scheduled to run.
    Return Values:
    -On Success:    the time
    """
    method_name = "runat"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


@onereturnvalue
def stop(job_name, p5_connection=None):
    """
    Syntax: Job <name> stop
    Description: Stops the scheduled job. Only jobs that have the scheduled
    status can be stopped. An attempt to stop a job with a different status
    will result in an error.
    Return Values:
    -On Success:    the string "1" if the job is stopped
                    the string "0" if the job could not be stopped
                    for whatever reason
    """
    method_name = "stop"
    return exec_nsdchat([module_name, job_name, method_name], p5_connection)


class Job(P5Resource):
    def __init__(self, job_name, p5_connection=None):
        super().__init__(job_name, p5_connection)

    def names(as_object=True, p5_connection=None):
        """
        Syntax: Job names
        Description: Returns a list of all currently scheduled or running jobs
        Return Values:
        -On Success:    the names of currently scheduled or running jobs
                        the string "<empty>" if no jobs are scheduled
        """
        method_name = "names"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, p5_connection)

    def completed(lastdays=None, as_object=True, p5_connection=None):
        """
        Syntax: Job completed [<lastdays>]
        Description: Returns the names of all jobs completed by the system.
        If the optional  <lastdays> argument is not given, jobs completed today
        are returned.
        Otherwise, all completed jobs for the last <lastdays> days are
        returned. The <lastdays> argument is interpreted as a positive integer
        (the default is 0 meaning today).
        Return Values:
        -On Success:    the names of completed jobs or
                        the string "<empty>" if no jobs completed
                        in the given time.
        """
        method_name = "completed"
        result = exec_nsdchat([module_name, method_name, lastdays],
                              p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, p5_connection)

    @onereturnvalue
    def completion(self):
        """
        Syntax: Job <name> completion
        Description: Returns the completion code of the completed job. The
        completion code can be one of:
            • success
            • exception
            • failure
        The success completion code means that the job has completed
        successfully in its entirety. It does not mean that all of the files
        have been archived and/or restored, though. For info about the
        particular file, use the protocol method.
        The exception completion code means that parts of the job have failed,
        but the job may have been partially executed successfully. This happens
        for parallel archive/restore operations where one of the job threads
        runs into an error, while others continue to run and finish
        successfully. The failure completion code means that the job has failed
        in its entirety and none of the files have been processed
        (archived/restored) correctly.
        Return Values:
        -On Success:    one of the completion codes
        """
        method_name = "completion"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def describe(self):
        """
        Syntax: Job <name> describe
        Description: Returns a (human readable) job description as shown in the
        P5 job monitor.
        Return Values:
        -On Success:    the job description
        """
        method_name = "describe"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def failed(lastdays=None, as_object=True, p5_connection=None):
        """
        Syntax: Job failed [<lastdays>]
        Description: Returns the names of all the jobs that failed to execute.
        If no optional argument <lastdays> is given, it returns jobs that
        failed today.
        Otherwise, all failed jobs for the last <lastdays> days are returned.
        The <lastdays> argument is interpreted as a positive integer
        (0 means today).
        Return Values:
        -On Success:    the names of failed jobs
                        the string "<empty>" if no jobs failed
        """
        method_name = "failed"
        result = exec_nsdchat([module_name, method_name, lastdays],
                              p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, p5_connection)

    @onereturnvalue
    def inventory(self, outputfile, options=None):
        """
        Syntax: Job <name> inventory <output file> [<options>]
        Description: Outputs a list of the files saved by the Archive-Job
        <name> into a file.
        The <output file> must be in the form [client:]absolute_path whereby
        client is the name of the P5 client where to store the file and
        absolute_path is the complete path to the file to hold the output. The
        client part is optional and defaults to localhost:
        The inventory command fills in the passed file with lines containing
        records separated by a TAB. If no <options> are given, the output file
        will by default contain the index paths of all the files saved by the
        given job <name>, one record per line. Additional <options> represent
        the attributes that will be output for each file in a tab-separated
        format. These attributes may be system attributes or any user-defined
        meta-data fields.
        The supported system attributes are:

        ppath:
        volumes:

        size:
        handle:
        btime:
        mtime:
        ino:
        the physical path of the file on the filesystem
        a blank separated list of the volumes where the file is saved
        the size of the saved file
        the handle as required by the RestoreSelection
        the backup time of the file
        the file's modification time
        the inode number of the file

        The index path returned by the inventory command cannot be used to
        access files on the file system in general. There are special cases
        where this might be used for this purpose, but generally it is not
        supported. The idea behind this info is to have an overview or idea
        what is being stored in the index and not to consume it in some other
        fashion (i.e. address the files on the file system to post-process
        them).
        In cases where files are still expected to be in the file system at the
        place they were at the point of archiving (for example somebody wants
        to delete them or otherwise post-process them) the ppath attribute may
        be used, which, when given on the command line, will yield the physical
        path as-found on the client where the file resides. Note that not all
        index entries have corresponding physical paths. In such cases the
        value will be set to the string "<empty>".
        Return Values:
        -On Success:    the <client>:<output file>
        """
        method_name = "inventory"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, outputfile,
                                                options])

    @onereturnvalue
    def label(self):
        """
        Syntax: Job <name> label
        Description: Returns the (human readable) job label.
        The following labels are returned:
        Archive, Backup, Synchronize and System.
        A Job label can be used in conjunction with the Job describe command to
        better display the job record in various list displays.
        Return Values:
        -On Success:    the job label
        """
        method_name = "label"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def pending(as_object=True, p5_connection=None):
        """
        Syntax: Job pending
        Description: Returns the names of all the jobs waiting to be executed,
        i.e. jobs that are still in the queue waiting to be scheduled and jobs
        that are already scheduled but wait for the next free worker thread.
        Return Values:
        -On Success:    the names of currently waiting jobs
                        the string "<empty>" if no jobs are waiting
        """
        method_name = "pending"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, p5_connection)

    @onereturnvalue
    def protocol(self, archiveentry=None):
        """
        Syntax: Job <name> protocol [<archiveentry>]
        Description: Returns a completion protocol of the completed job and/or
        of one of the archived and/or restored file(s) given by the optional
        <archiveentry> argument. The protocol contains human readable text.
        Return Values:
        -On Success:    the requested protocol
        """
        method_name = "protocol"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name, archiveentry])

    @onereturnvalue
    def report(self):
        """
        Syntax: Job <name> report
        Description: Returns a report of the currently running job. The report
        contains human readable text.
        Return Values:
        -On Success:    the report text
        """
        method_name = "report"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def resourcegroup(self):
        """
        Syntax: Job <name> resourcegroup
        Description: Returns the name of the resource group for which this job
        has been running.
        Return Values:
        -On Success:    the name of the resource group
                        (for example ArchivePlan, SyncPlan, etc.)
                        or the string "<empty>",
                        if no resource group is associated with the job
        """
        method_name = "resourcegroup"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def resourcename(self):
        """
        Syntax: Job <name> resourcename
        Description: Returns the name of the resource for which this job has
        been running
        Return Values:
        -On Success:    the name of the resource
                        (for example Default-Backup, Default-Archive)
                        or the string "<empty>",
                        if no resource group is associated with the job
        """
        method_name = "resourcename"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def running(as_object=True, p5_connection=None):
        """
        Syntax: Job running
        Description: Returns the names of all currently running jobs.
        Return Values:
        -On Success:    the names of currently running jobs
                        the string "<empty>" if no jobs are running
        """
        method_name = "running"
        result = exec_nsdchat([module_name, method_name], p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, p5_connection)

    @onereturnvalue
    def status(self):
        """
        Syntax: Job <name> status
        Description: Returns the status of the job. A job can have a number of
        internal statuses, depending on the stage of the archive and/or restore
        process. Currently, the following statuses are supported:
            • started   the job is starting (intermediate state)
            • stopped   the job is stopping (intermediate state)
            • unknown   the job is not known by the system
            • scheduled the job is in the queue waiting to be run
            • pending   an intermediate state during start,
                        the job is waiting to be accepted for start
                        by the queue manager
            • running   the job is running
            • canceled  the job is canceled by user
            • completed the job is completed
            • terminated        the job is terminated by a server shutdown
        Return Values:
        -On Success:    one of the supported statuses
        """
        method_name = "status"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def warning(lastdays=None, as_object=True, p5_connection=None):
        """
        Syntax: Job warning [<lastdays>]
        Description: Returns names of all jobs with warnings. If no optional
        argument <lastdays> is given, it returns jobs with warnings from today.
        Otherwise, all jobs with warnings for the last <lastdays> days are
        returned.
        The <lastdays> argument is interpreted as a positive integer
        (0 = today).
        Return Values:
        -On Success:    the names of jobs with warnings
                        the string "<empty>" if no jobs ended with a warning
        """
        method_name = "warning"
        result = exec_nsdchat([module_name, method_name, lastdays],
                              p5_connection)
        if not as_object:
            return result
        else:
            return resourcelist(result, Job, p5_connection)

    @onereturnvalue
    def xmlticket(self, outputfile=None):
        """
        Syntax: Job <name> xmlticket [<outfilename>]
        Description: Returns the completion protocol of the completed job.
        The protocol contains human readable text embedded in generic XML
        sections.
        If the optional <outfilename> argument is given, the output of the
        command is rerouted to the given file.
        Return Values:
        -On Success:    the requested protocol
        """
        method_name = "xmlticket"
        outputfile_option = ""
        if outputfile:
            outputfile_option = outputfile
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name,
                                                outputfile_option])

    @onereturnvalue
    def cancel(self):
        """
        Syntax: Job <name> cancel
        Description: Cancels the running job. Only jobs that have the running
        status can be canceled. An attempt to cancel a job with a different
        status will result in an error.
        Return Values:
        -On Success:    the string "1" if the job is canceled
                        the string "0" if the job could not be canceled
                        for whatever reason
        """
        method_name = "cancel"
        return self.p5_connection.nsdchat_call([module_name, job_name,
                                                method_name])

    @onereturnvalue
    def runat(self):
        """
        Syntax: Job <name> runat
        Description: Returns the time in seconds (Posix time) when the job was
        scheduled to run.
        Return Values:
        -On Success:    the time
        """
        method_name = "runat"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    @onereturnvalue
    def stop(self):
        """
        Syntax: Job <name> stop
        Description: Stops the scheduled job. Only jobs that have the scheduled
        status can be stopped. An attempt to stop a job with a different status
        will result in an error.
        Return Values:
        -On Success:    the string "1" if the job is stopped
                        the string "0" if the job could not be stopped
                        for whatever reason
        """
        method_name = "stop"
        return self.p5_connection.nsdchat_call([module_name, self.name,
                                                method_name])

    def __repr__(self):
        return ": ".join([module_name, self.name])
