import client from './client';

export const getDashboard = () => client.get('/student/dashboard');
export const getMastery = () => client.get('/student/mastery');
export const getProgress = () => client.get('/student/progress');
export const joinClass = (classCode) => client.post('/student/join-class', { class_code: classCode });
export const getStudentClass = () => client.get('/student/class');
