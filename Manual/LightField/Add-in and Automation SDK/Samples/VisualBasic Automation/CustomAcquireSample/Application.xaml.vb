Class Application

    ' Application-level events, such as Startup, Exit, and DispatcherUnhandledException
    ' can be handled in this file.

    Protected Overrides Sub OnSessionEnding(e As System.Windows.SessionEndingCancelEventArgs)
        'Cancelling because we can't guarantee proper cleanup of automated LF's 
        'unless the automating application is closed directly.
        e.Cancel = True
        MyBase.OnSessionEnding(e)
    End Sub
End Class
