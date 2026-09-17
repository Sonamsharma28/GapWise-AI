import client from './client';

export const startAssessment = (data) => client.post('/assessment/start', data);
export const submitAssessment = (id, data) => client.post(`/assessment/${id}/submit`, data);
export const getReport = (id) => client.get(`/assessment/${id}/report`);
export const getHistory = () => client.get('/assessment/history');
