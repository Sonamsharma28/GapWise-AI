import client from './client';

export const getDashboard = () => client.get('/teacher/dashboard');
export const getStudents = () => client.get('/teacher/students');
export const getStudentDetail = (id) => client.get(`/teacher/student/${id}`);
export const createClass = (data) => client.post('/teacher/classes', data);
export const getTeacherClasses = () => client.get('/teacher/classes');
export const getClassDetail = (classId) => client.get(`/teacher/classes/${classId}`);
