#include <pthread.h>
#include <stdio.h>
#include <stdlib.h> 

#define NUMBER_OF_THREADS   10

void *print_hello_world(void *tid){
    printf("Hello World. Greetings from thread: %d\n",tid);
    // pthread_attr_destroy();
    pthread_exit(NULL);

}

int main(int argc, char *argv[]){
    pthread_t threads[NUMBER_OF_THREADS];
    int status, i;

    for (int i = 0; i < NUMBER_OF_THREADS; i++)
    {
        printf("Main Here. Creating thread %d\n", i);
        status = pthread_create(&threads[i], NULL, print_hello_world, (void *)i);

        if(status != 0){
            printf("Oooops, pthread_create returned eror code %d\n", status);
            exit(-1);
        }
    }
    exit(NULL);
    
}
