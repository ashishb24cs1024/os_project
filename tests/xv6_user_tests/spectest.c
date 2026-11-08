// user/spectest.c
// Test program for Problem 5: Externalization barriers for speculative processes

#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fcntl.h"

void test_abort_isolation(void) {
  printf("--- Test 1: Write and Abort Isolation ---\n");
  int fd = open("test_file.txt", O_CREATE | O_RDWR);
  write(fd, "initial_data\n", 13);
  close(fd);

  int pid = fork();
  if (pid == 0) {
    // Child enters speculative mode
    if (xbegin() < 0) {
      printf("xbegin failed\n");
      exit(1);
    }
    printf("Child: entered speculative mode\n");

    // Overwrite file speculatively
    fd = open("test_file.txt", O_RDWR);
    write(fd, "speculative_mod\n", 16);
    close(fd);

    // Read back own write
    char buf[32];
    fd = open("test_file.txt", O_RDONLY);
    int n = read(fd, buf, sizeof(buf) - 1);
    buf[n] = '\0';
    close(fd);
    printf("Child (inside spec) read: %s", buf);

    // Now abort
    printf("Child: aborting speculation...\n");
    xabort();
    exit(0);
  }

  wait(0);

  // Outside parent checks real file
  char buf[32];
  fd = open("test_file.txt", O_RDONLY);
  int n = read(fd, buf, sizeof(buf) - 1);
  buf[n] = '\0';
  close(fd);
  printf("Parent (outside spec) read: %s", buf);
  if (strcmp(buf, "initial_data\n") == 0) {
    printf("[PASS] Abort cleanly preserved original file state!\n");
  } else {
    printf("[FAIL] File was corrupted by aborted speculation!\n");
  }
}

int main(int argc, char *argv[]) {
  printf("Starting Speculative Execution Tests...\n");
  test_abort_isolation();
  exit(0);
}
