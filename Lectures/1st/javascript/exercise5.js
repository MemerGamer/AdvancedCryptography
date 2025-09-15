/**
 * Advanced Cryptography Exercise 5: Safe SQL Insertion
 * Author: AI Assistant
 * Methods used: AI assistance
 *
 * This file contains a JavaScript function for safely inserting data into a SQL database
 * while preventing SQL injection attacks.
 */

/**
 * Safely adds a new student record to the DIÁKOK table
 *
 * @param {string} name - The student's name
 * @param {number} age - The student's age
 * @param {Object} dbConnection - Database connection object
 * @returns {Promise<Object>} - Result object with success status and data
 *
 * Method: AI assistance
 */
async function addStudent(name, age, dbConnection) {
  // Input validation
  if (!name || typeof name !== "string") {
    throw new Error("Name must be a non-empty string");
  }

  if (!Number.isInteger(age) || age < 0 || age > 150) {
    throw new Error("Age must be a valid integer between 0 and 150");
  }

  // Trim whitespace and validate length
  const trimmedName = name.trim();
  if (trimmedName.length === 0) {
    throw new Error("Name cannot be empty after trimming");
  }

  if (trimmedName.length > 100) {
    throw new Error("Name is too long (max 100 characters)");
  }

  try {
    // Use parameterized query to prevent SQL injection
    // This is the key security feature - parameters are handled safely by the database driver
    const query = "INSERT INTO DIÁKOK (NÉV, KOR) VALUES (?, ?)";
    const params = [trimmedName, age];

    // Execute the query with parameters
    const result = await dbConnection.execute(query, params);

    return {
      success: true,
      message: "Student added successfully",
      data: {
        id: result.insertId,
        name: trimmedName,
        age: age,
      },
    };
  } catch (error) {
    console.error("Database error:", error);
    throw new Error(`Failed to add student: ${error.message}`);
  }
}

/**
 * Mock database connection for demonstration purposes
 * In real applications, this would be replaced with actual database drivers like:
 * - mysql2 for MySQL
 * - pg for PostgreSQL
 * - sqlite3 for SQLite
 *
 * Method: AI assistance
 */
class MockDatabaseConnection {
  constructor() {
    this.students = []; // In-memory storage for demo
    this.nextId = 1;
  }

  async execute(query, params) {
    console.log("Executing query:", query);
    console.log("With parameters:", params);

    // Simulate INSERT operation
    if (query.includes("INSERT INTO DIÁKOK")) {
      const [name, age] = params;
      const student = {
        id: this.nextId++,
        name: name,
        age: age,
      };
      this.students.push(student);

      return {
        insertId: student.id,
        affectedRows: 1,
      };
    }

    throw new Error("Unsupported query");
  }

  // Helper method to view all students (for demo)
  getAllStudents() {
    return this.students;
  }
}

/**
 * Demonstration function showing how to use the addStudent function safely
 *
 * Method: AI assistance
 */
async function demonstrateUsage() {
  console.log("=== JavaScript Safe SQL Insertion Demo ===\n");

  const mockDb = new MockDatabaseConnection();

  const testCases = [
    // Valid data
    { name: "Kovács János", age: 20, description: "Valid student data" },
    { name: "Nagy Anna", age: 18, description: "Another valid student" },

    // Potentially malicious data (should be handled safely)
    {
      name: "'; DROP TABLE DIÁKOK; --",
      age: 25,
      description: "SQL injection attempt",
    },
    {
      name: "Robert'; DELETE FROM DIÁKOK WHERE '1'='1",
      age: 22,
      description: "Another injection attempt",
    },

    // Invalid data (should throw errors)
    { name: "", age: 20, description: "Empty name" },
    { name: "Valid Name", age: -5, description: "Invalid age" },
    { name: "Valid Name", age: 200, description: "Age too high" },
  ];

  for (let i = 0; i < testCases.length; i++) {
    const { name, age, description } = testCases[i];

    console.log(`${i + 1}. Testing: ${description}`);
    console.log(`   Input: name="${name}", age=${age}`);

    try {
      const result = await addStudent(name, age, mockDb);
      console.log(`   Result: ✅ ${result.message}`);
      console.log(`   Data: ${JSON.stringify(result.data)}`);
    } catch (error) {
      console.log(`   Result: ❌ Error - ${error.message}`);
    }

    console.log();
  }

  // Show all students that were successfully added
  console.log("All students in database:");
  console.table(mockDb.getAllStudents());
}

/**
 * Real-world example with MySQL (commented out - requires mysql2 package)
 *
 * Method: AI assistance + Internet research
 */
/*
async function addStudentMySQL(name, age) {
  const mysql = require('mysql2/promise');
  
  const connection = await mysql.createConnection({
    host: 'localhost',
    user: 'your_username',
    password: 'your_password',
    database: 'your_database'
  });

  try {
    const result = await addStudent(name, age, connection);
    return result;
  } finally {
    await connection.end();
  }
}
*/

/**
 * Real-world example with PostgreSQL (commented out - requires pg package)
 *
 * Method: AI assistance + Internet research
 */
/*
async function addStudentPostgreSQL(name, age) {
  const { Client } = require('pg');
  
  const client = new Client({
    user: 'your_username',
    host: 'localhost',
    database: 'your_database',
    password: 'your_password',
    port: 5432,
  });

  await client.connect();

  try {
    // PostgreSQL uses $1, $2 for parameters instead of ?
    const adaptedConnection = {
      async execute(query, params) {
        const pgQuery = query.replace(/\?/g, (match, index) => `$${params.indexOf(params[index]) + 1}`);
        const result = await client.query(pgQuery, params);
        return {
          insertId: result.rows[0]?.id,
          affectedRows: result.rowCount
        };
      }
    };

    const result = await addStudent(name, age, adaptedConnection);
    return result;
  } finally {
    await client.end();
  }
}
*/

// Export functions for use in other modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    addStudent,
    MockDatabaseConnection,
    demonstrateUsage,
  };
}

// Run demonstration if this file is executed directly
if (typeof require !== "undefined" && require.main === module) {
  demonstrateUsage();
}
