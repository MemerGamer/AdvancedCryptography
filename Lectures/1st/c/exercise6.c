/**
 * Advanced Cryptography Exercise 6: Integer to Formatted String
 * Author: AI Assistant
 * Methods used: AI assistance
 *
 * This file contains a C function that converts a signed integer to a formatted string
 * with comma separators (e.g., 7000000 -> "7,000,000").
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

/**
 * Converts a signed integer to a formatted string with comma separators
 *
 * @param num The signed integer to convert
 * @return A dynamically allocated string with the formatted number
 *         The caller is responsible for freeing the returned string
 *
 * Method: AI assistance
 */
char *format_integer(int num)
{
    // Handle zero as special case
    if (num == 0)
    {
        char *result = malloc(2);
        if (!result)
            return NULL;
        strcpy(result, "0");
        return result;
    }

    // Determine if number is negative
    int is_negative = (num < 0);

    // Handle INT_MIN safely - use long long to avoid overflow
    long long abs_num = (long long)num;
    if (abs_num < 0)
    {
        abs_num = -abs_num;
    }

    // Count digits
    long long temp = abs_num;
    int digit_count = 0;
    while (temp > 0)
    {
        digit_count++;
        temp /= 10;
    }

    // Calculate commas needed and total string length
    int comma_count = (digit_count - 1) / 3;
    int total_length = digit_count + comma_count + (is_negative ? 1 : 0) + 1;

    // Allocate memory
    char *result = malloc(total_length);
    if (!result)
        return NULL;

    // Build string from right to left
    int pos = total_length - 1;
    result[pos--] = '\0'; // Null terminator

    int digits_written = 0;
    while (abs_num > 0)
    {
        // Add comma every 3 digits (except before the first digit)
        if (digits_written > 0 && digits_written % 3 == 0)
        {
            result[pos--] = ',';
        }

        // Add digit
        result[pos--] = '0' + (abs_num % 10);
        abs_num /= 10;
        digits_written++;
    }

    // Add negative sign if needed
    if (is_negative)
    {
        result[pos] = '-';
    }

    return result;
}

/**
 * Test function to demonstrate the integer formatting
 *
 * Method: AI assistance
 */
void test_format_integer()
{
    printf("=== C Integer Formatting Demo ===\n\n");

    // Test cases including edge cases
    int test_cases[] = {
        0,
        1,
        12,
        123,
        1234,
        12345,
        123456,
        1234567,
        12345678,
        123456789,
        1000000000,
        7000000,  // Example from exercise
        -7000000, // Negative version
        -123456,
        2147483647, // INT_MAX
        -2147483648 // INT_MIN
    };

    int num_test_cases = sizeof(test_cases) / sizeof(test_cases[0]);

    printf("Testing format_integer function:\n");
    printf("Input Number -> Formatted Output\n");
    printf("--------------------------------\n");

    for (int i = 0; i < num_test_cases; i++)
    {
        char *formatted = format_integer(test_cases[i]);
        if (formatted)
        {
            printf("%12d -> \"%s\"\n", test_cases[i], formatted);
            free(formatted); // Important: free allocated memory
        }
        else
        {
            printf("%12d -> ERROR: Memory allocation failed\n", test_cases[i]);
        }
    }
}

/**
 * Interactive test function allowing user input
 *
 * Method: AI assistance
 */
void interactive_test()
{
    printf("\n=== Interactive Test ===\n");
    printf("Enter integers to format (or 'q' to quit):\n");

    char input[20];
    while (1)
    {
        printf("\nEnter number: ");
        if (!fgets(input, sizeof(input), stdin))
        {
            break;
        }

        // Remove newline
        input[strcspn(input, "\n")] = '\0';

        // Check for quit
        if (strcmp(input, "q") == 0 || strcmp(input, "quit") == 0)
        {
            printf("Goodbye!\n");
            break;
        }

        // Convert and validate
        char *endptr;
        long num = strtol(input, &endptr, 10);

        // Check for valid conversion and range
        if (*endptr != '\0')
        {
            printf("Error: Invalid input '%s'. Please enter a valid integer.\n", input);
            continue;
        }

        if (num < INT_MIN || num > INT_MAX)
        {
            printf("Error: Number %ld is out of range for int (%d to %d).\n",
                   num, INT_MIN, INT_MAX);
            continue;
        }

        // Format and display
        char *formatted = format_integer((int)num);
        if (formatted)
        {
            printf("%d -> \"%s\"\n", (int)num, formatted);
            free(formatted);
        }
        else
        {
            printf("Error: Memory allocation failed\n");
        }
    }
}

/**
 * Main function
 *
 * Method: AI assistance
 */
int main()
{
    test_format_integer();
    interactive_test();
    return 0;
}