// please write a code in js to manage students info
/*
you are js developer
The university composed of a collection of Students.
Each Student has name, faculty and a collection of grades.
Any student can add a new grade (must NOT be negative), calculate the
grades avg and can change faculty
The University can add and remove students, calculate the avg of all
students grades avges and find the most excellent student.

*/
// The current implementation uses a Map to store students in the University class.
// This is a good choice because it allows efficient addition, removal, and lookup of students by their name.
// If you need to frequently search or sort students based on other attributes (e.g., faculty or grades), 
// you might consider using an array of objects instead, with additional indexing or sorting logic.
// However, for the current requirements, the Map data structure is appropriate and efficient.  

class Student {
    constructor(name, faculty) {
        this.name = name;
        this.faculty = faculty;
        this.grades = [];
    }

    /**
     * Adds a grade to the grades array if it is non-negative.
     * Logs a message to the console if the grade is negative.
     *
     * @param {number} grade - The grade to be added. Must be a non-negative number.
     */
    addGrade(grade) {
        if (grade >= 0) {
            this.grades.push(grade);
        } else {
            console.log("Grade must NOT be negative");
        }
    }

    calculateAvg() {
        if (this.grades.length === 0) return 0;
        const sum = this.grades.reduce((acc, curr) => acc + curr, 0);
        return sum / this.grades.length;
    }

    changeFaculty(newFaculty) {
        this.faculty = newFaculty;
    }
}

class University {
    constructor() {
        this.students = new Map();
    }

    addStudent(student) {
        this.students.set(student.name, student);
    }

    removeStudent(studentName) {
        this.students.delete(studentName);
    }

    calculateOverallAvg() {
        if (this.students.size === 0) return 0;
        const totalAvg = Array.from(this.students.values()).reduce((acc, student) => acc + student.calculateAvg(), 0);
        return totalAvg / this.students.size;
    }

    findMostExcellentStudent() {
        // `this.students` is a Map; convert to an array of Student values first
        if (this.students.size === 0) return null;
        const studentsArr = Array.from(this.students.values());
        return studentsArr.reduce((best, student) => {
            return student.calculateAvg() > best.calculateAvg() ? student : best;
        }, studentsArr[0]);
    }
}

// Example usage:
const uni = new University();

const student1 = new Student("Alice", "Engineering");
student1.addGrade(90);
student1.addGrade(85);

const student2 = new Student("Bob", "Science");
student2.addGrade(95);
student2.addGrade(80);

uni.addStudent(student1);
uni.addStudent(student2);

console.log("Overall Average:", uni.calculateOverallAvg());
const excellentStudent = uni.findMostExcellentStudent();
if (excellentStudent) {
    console.log("Most Excellent Student:", excellentStudent.name);
} else {
    console.log("Most Excellent Student: None");
}