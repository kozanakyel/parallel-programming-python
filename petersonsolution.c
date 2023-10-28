#include <stdio.h>
#include <pthread.h>

#define FALSE 0
#define TRUE 1
#define N 2                                                 /* number of processes */

/**
 * This Peterson solution and TSL instructio for test and set processes require BUSY WAITING.
 * Line  while(.......) represents the BUSY WAITING for our solution and it needs 
 * extra CPU resources taht is not good. But solution is correct...
*/


/**
 * PRIORITY INVERSION PROBLEM: if process has the priority knowledge
 * for entering the Critical Regions. H and L.... Sleep and Wakeup...
*/


int turn;                                                   /* whose turn is it? */
int interested[N];                                          /* all values initially 0 (FALSE) */

void enter_region(int process)                              /* process is 0 or 1 */
{
    int other;                                              /* number of the other process */
    other = 1 - process;                                    /* the opposite of process */
    interested[process] = TRUE;                             /* show that you are interested */
    turn = process;                                         /* set flag */
    while (turn == process && interested[other] == TRUE) 
        ;                                                   /* null statement */ 
};

void leave_region(int process)                              /* process: who is leaving */
{
    interested[process] = FALSE;                            /* indicate departure from critical region */
};


void *process_function(void *arg) {
    int process_id = *((int *)arg);

    // Enter critical region
    enter_region(process_id);

    // Critical section (replace this with your actual critical section code)
    printf("Process %d is in the critical section.\n", process_id);

    // Leave critical region
    leave_region(process_id);

    pthread_exit(NULL);
}

int main() {
    pthread_t threads[N];
    int thread_ids[N];

    // Initialize thread IDs
    for (int i = 0; i < N; i++) {
        thread_ids[i] = i;
    }

    // Create threads
    for (int i = 0; i < N; i++) {
        if (pthread_create(&threads[i], NULL, process_function, (void *)&thread_ids[i]) != 0) {
            fprintf(stderr, "Error creating thread %d\n", i);
            return 1;
        }
    }

    // Join threads
    for (int i = 0; i < N; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            fprintf(stderr, "Error joining thread %d\n", i);
            return 1;
        }
    }

    return 0;
}

