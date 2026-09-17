import client from './client';

export const sendMessage = (message, concept_id = null, question_id = null, question_num = null) => {
  if (typeof message === 'object') {
    return client.post('/ai/mentor', message);
  }
  return client.post('/ai/mentor', {
    message,
    concept_id,
    question_id,
    question_num
  });
};

/** Fetches a structured step-by-step AI explanation for a specific wrong question. */
export const getQuestionExplanation = (questionId) => {
  return client.get(`/ai/explain/${questionId}`);
};
