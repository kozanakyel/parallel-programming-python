#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdint.h> // Include this for intptr_t

#define NUMBER_OF_THREADS 10

void *print_hello_world(void *tid) {
    printf("Hello World. Greetings from thread: %ld\n", (intptr_t)tid);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUMBER_OF_THREADS];
    int status, i;

    for (i = 0; i < NUMBER_OF_THREADS; i++) {
        printf("Main Here. Creating thread %d\n", i);
        status = pthread_create(&threads[i], NULL, print_hello_world, (void *)(intptr_t)i);

        if (status != 0) {
            printf("Oops, pthread_create returned error code %d\n", status);
            exit(-1);
        }
    }

    for (i = 0; i < NUMBER_OF_THREADS; i++) {
        status = pthread_join(threads[i], NULL);
        if (status != 0) {
            printf("Oops, pthread_join returned error code %d\n", status);
            exit(-1);
        }
        printf("Main Here. Joined with thread %d\n", i);
    }

    for (i = 0; i < NUMBER_OF_THREADS; i++) {
        status = pthread_detach(threads[i]);
        if (status != 0) {
            printf("Oops, pthread_detach returned error code %d\n", status);
            exit(-1);
        }
    }

    printf("Main Here. All threads joined and cleaned up.\n");
    pthread_exit(NULL);
}