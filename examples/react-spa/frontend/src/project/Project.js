import React, { useState, useEffect } from 'react';
import axiosInstance from './axiosConfig';
import './Project.css';

function Project() {
  const [projects, setProjects] = useState([]); 
  const [newProject, setNewProject] = useState({ name: '', description: '', estimate_time: 0 }); 
  const [editProject, setEditProject] = useState(null); 
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState(null); 

  // Fetch projects on component mount
  useEffect(() => {
    fetchProjects();
  }, []);

  // Fetch all projects (List of all)
  const fetchProjects = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/task/project/list/');
      setProjects(response.data);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to fetch projects.');
    } finally {
      setLoading(false);
    }
  };

  // For create a new project 
  const createProject = async () => {
    setLoading(true);
    try {
      await axiosInstance.post('/task/project/create/', newProject);
      setNewProject({ name: '', description: '', estimate_time: 0 });
      fetchProjects(); // Refresh project list
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create project.');
    } finally {
      setLoading(false);
    }
  };

  // Update an existing project
  const updateProject = async () => {
    if (!editProject) return; // Prevent update if no project is being edited

    setLoading(true);
    try {
      await axiosInstance.put(`/task/project/update/${editProject.id}/`, editProject);
      setEditProject(null); // Exit edit mode
      fetchProjects(); // Refresh project list
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to update project.');
    } finally {
      setLoading(false);
    }
  };

  // Delete a project
  const deleteProject = async (id) => {
    setLoading(true);
    try {
      await axiosInstance.delete(`/task/project/delete/${id}/`);
      fetchProjects(); // Refresh project list
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to delete project.');
    } finally {
      setLoading(false);
    }
  };

  // Start editing a project
  const startEditing = (project) => {
    setEditProject({ ...project }); // Copy the project for editing
  };

  // Handle changes in the edit form
  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditProject((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="project-container">
      <h1>Task Project Management</h1>

      
      {error && <p className="error-message">{error}</p>}

      
      <div className="form-container">
        <h3>Create New Project</h3>
        <input
          type="text"
          placeholder="Name"
          value={newProject.name}
          onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={newProject.description}
          onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
        />
        <input
          type="number"
          placeholder="Estimate Time (hours)"
          value={newProject.estimate_time}
          onChange={(e) => setNewProject({ ...newProject, estimate_time: e.target.value })}
        />
        <button className="create-button" onClick={createProject} disabled={loading}>
          {loading ? 'Creating...' : 'Create'}
        </button>
      </div>

      {editProject && (
        <div className="form-container">
          <h3>Edit Project</h3>
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={editProject.name}
            onChange={handleEditChange}
          />
          <input
            type="text"
            name="description"
            placeholder="Description"
            value={editProject.description}
            onChange={handleEditChange}
          />
          <input
            type="number"
            name="estimate_time"
            placeholder="Estimate Time (hours)"
            value={editProject.estimate_time}
            onChange={handleEditChange}
          />
          <button className="create-button" onClick={updateProject} disabled={loading}>
            {loading ? 'Updating...' : 'Update'}
          </button>
          <button className="create-button" onClick={() => setEditProject(null)} disabled={loading}>
            Cancel
          </button>
        </div>
      )}

      <div className="project-list">
        <h3>Project List</h3>
        {loading && <p>Loading projects...</p>}
        {projects.map((project) => (
          <div className="project-card" key={project.id}>
            <h4>{project.name}</h4>
            <p>{project.description}</p>
            <p>Estimate Time: {project.estimate_time} hours</p>
            <button className="update-button" onClick={() => startEditing(project)} disabled={loading}>
              Edit
            </button>
            <button className="delete-button" onClick={() => deleteProject(project.id)} disabled={loading}>
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Project;
