import client from './client';

export const getConcepts = () => client.get('/graph/concepts');
