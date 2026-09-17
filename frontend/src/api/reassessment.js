import client from './client';

export const startReassessment = () => client.post('/reassessment/start');
export const submitReassessment = (id, data) => client.post(`/reassessment/${id}/submit`, data);
export const getComparison = (id) => client.get(`/reassessment/${id}/comparison`);
