// Inspired by: https://gist.github.com/3019549
// You need to have enabled access for assistive devices in:
//      System Preferences/Universal Access
// Compile using:
//      clang -o keys keys.m -framework cocoa

#import <Cocoa/Cocoa.h>

@interface AppDelegate : NSObject <NSApplicationDelegate>
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [NSEvent addGlobalMonitorForEventsMatchingMask:NSKeyDownMask
                                           handler:^(NSEvent *event){
        NSDate* now = [[NSDate alloc] init];
        NSDateFormatter* format = [[NSDateFormatter alloc] init];
        [format setDateFormat:@"c,yy,MM,dd,HH,mm,ss,Z"];

        // Find the currently running app.
        NSRunningApplication* app = [[NSWorkspace sharedWorkspace] frontmostApplication];
        NSArray* runningApps = [[NSWorkspace sharedWorkspace] runningApplications];
        NSString* appName = [app localizedName];
        NSString* update = [NSString stringWithFormat: @"%d,%@,'%@'\n",
                event.keyCode, [format stringFromDate: now], appName];
        FILE* f = fopen([[NSHomeDirectory() stringByAppendingString: @"/.keys"]
                                                            UTF8String], "a");
        fprintf(f, "%s", [update UTF8String]);
        fclose(f);

        [now release];
        [format release];
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
