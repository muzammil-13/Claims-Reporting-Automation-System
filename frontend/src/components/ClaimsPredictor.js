import React, { useState } from 'react';
import { predictClaims } from '../api/reports';

const ClaimsPredictor = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setResults(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await predictClaims(file);
      setResults(data);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        err.message || 
        'An error occurred while processing your file'
      );
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString();
    } catch {
      return dateString;
    }
  };

  const formatCurrency = (amount) => {
    if (amount === null || amount === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatPercent = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">
          Claims Prediction (ML Model)
        </h2>
        <p className="text-gray-600 mb-6">
          Upload a CSV/TXT file with claims data to predict outcomes for pending claims.
          The model will analyze historical patterns and predict whether pending claims
          will be Paid or Denied.
        </p>

        <form onSubmit={handleSubmit} className="mb-6">
          <div className="mb-4">
            <label
              htmlFor="file-input"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Select CSV/TXT File
            </label>
            <input
              id="file-input"
              type="file"
              accept=".csv,.txt"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100
                border border-gray-300 rounded-lg p-2"
              disabled={loading}
            />
            {file && (
              <p className="mt-2 text-sm text-gray-600">
                Selected: <span className="font-medium">{file.name}</span>
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || !file}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg
              font-semibold hover:bg-blue-700 disabled:bg-gray-400
              disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Processing...' : 'Predict Claims'}
          </button>
        </form>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">Error:</p>
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {results && (
          <div className="space-y-6">
            {/* Summary Section */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Total Claims</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {results.total_claims}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Training Claims</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {results.training_claims}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Pending Claims</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {results.pending_claims}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Predictions</p>
                  <p className="text-2xl font-bold text-green-600">
                    {results.predictions?.length || 0}
                  </p>
                </div>
              </div>

              {results.summary && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Paid: </span>
                      <span className="font-semibold text-green-600">
                        {results.summary.paid_count}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Denied: </span>
                      <span className="font-semibold text-red-600">
                        {results.summary.denied_count}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Pending: </span>
                      <span className="font-semibold text-orange-600">
                        {results.summary.pending_count}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Predictions Table */}
            {results.predictions && results.predictions.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
                <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
                  <h3 className="text-xl font-bold text-gray-800">
                    Predictions for Pending Claims
                  </h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Claim ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Amount
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Type
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Predicted Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Denial Probability
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Confidence
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {results.predictions.map((prediction, index) => (
                        <tr
                          key={index}
                          className="hover:bg-gray-50 transition-colors"
                        >
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {prediction.ClaimID}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {formatCurrency(prediction.Amount)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {prediction.Type}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {formatDate(prediction.Date)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                prediction.Predicted_Status === 'Denied'
                                  ? 'bg-red-100 text-red-800'
                                  : 'bg-green-100 text-green-800'
                              }`}
                            >
                              {prediction.Predicted_Status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            <div className="flex items-center">
                              <span className="mr-2">
                                {formatPercent(prediction.Denial_Probability)}
                              </span>
                              <div className="w-24 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-red-500 h-2 rounded-full"
                                  style={{
                                    width: `${(prediction.Denial_Probability || 0) * 100}%`,
                                  }}
                                />
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {formatPercent(prediction.Confidence)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {results.predictions && results.predictions.length === 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800">
                  No pending claims found in the uploaded file. All claims have been
                  processed (Paid or Denied).
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ClaimsPredictor;
