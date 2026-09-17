import client from './client';

export const getPath = () => client.get('/learning/path');
export const getConcept = (id) => client.get(`/learning/concept/${id}`);
export const getPracticeQuestions = (conceptId) => client.get(`/learning/practice`, { params: { concept_id: conceptId } });
export const submitPractice = (conceptId, data) => client.post(`/learning/practice/${conceptId}/submit`, data);
