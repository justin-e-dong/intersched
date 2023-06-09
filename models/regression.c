#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define DATA_FILENAME "./bt.parsed"
#define N 1299

// Calculate linear regression
void linear_regression(double *x, double *y, int n, double *slope, double *intercept)
{
    double sumXY = 0.0;
    double sumX = 0.0;
    double sumY = 0.0;
    double sumX2 = 0.0;

    int i;

    for (i = 0; i < n; i++)
    {
        sumXY += x[i] * y[i];
        sumX += x[i];
        sumY += y[i];
        sumX2 += x[i] * x[i];
    }

    *slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    *intercept = (sumY - (*slope) * sumX) / n;
}

// Takes in 1 argument: the number of interrupts to include in the linear regression
int main(int argc, char *argv[])
{
    // Read arguments
    int argi = 0;
    const int n = atoi(argv[++argi]); // Window size

    // Initialize variables to calculate the number of sections

    // Open the file for reading
    FILE *file = fopen(DATA_FILENAME, "r");
    if (file == NULL)
    {
        printf("Error opening the file.\n");
        return 1;
    }

    // Allocate memory
    double *x = (double *)malloc(N * sizeof(double));
    double *y = (double *)malloc(N * sizeof(double));

    // Get data from file
    char *line;
    int index = 0;
    size_t line_length = 0;
    while (index < N && getline(&line, &line_length, file) != -1)
    {
        double value = strtod(line, NULL);
        x[index] = index;
        y[index] = value;
        index++;
    }

    // Free line
    free(line);

    // Start clock
    struct timespec start_time;
    clock_gettime(CLOCK_REALTIME, &start_time);

    // Calculations
    double slope, intercept;
    linear_regression(x, y, n, &slope, &intercept);

    // Calculate Elapsed Time
    struct timespec end_time;
    clock_gettime(CLOCK_REALTIME, &end_time);
    long long elapsed_time = (end_time.tv_sec - start_time.tv_sec) * 1000000000LL +
                             (end_time.tv_nsec - start_time.tv_nsec);

    // Print results
    printf("Linear Regression Model: y = %.6fx + %.6f\n", slope, intercept);
    printf("Calculation Time: %lld nanoseconds\n", elapsed_time);

    // Free memory
    free(x);
    free(y);
    fclose(file);

    return 0;
}