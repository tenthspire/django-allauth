import React, { useState, useEffect } from 'react';
import axios from './axiosConfig'; 
import './domain.css'

const DomainPurchasePage = () => {
    const [domains, setDomains] = useState([]);
    const [contactInfo, setContactInfo] = useState({});
    const [domainName, setDomainName] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        axios.get('list-domain-purchases/')
            .then(response => {
                setDomains(response.data);
            })
            .catch(error => {
                setError('Error fetching domain data');
            });
    }, []);

    const handleUpdate = (domainName) => {
        if (!domainName || !contactInfo) {
            setError('Please provide both domain name and contact info');
            return;
        }

        axios.post('update-domain-contact/', { domain_name: domainName, contact_info: contactInfo })
            .then(response => {
                alert('Domain updated successfully');
                setError('');
                setContactInfo({});
                axios.get('list-domain-purchases/')
                    .then(response => {
                        setDomains(response.data);
                    });
            })
            .catch(error => {
                setError('Error updating domain');
            });
    };

    const handleContactInfoChange = (e) => {
        try {
            const parsedContactInfo = JSON.parse(e.target.value);
            setContactInfo(parsedContactInfo);
            setError(''); 
        } catch (error) {
            setError('Invalid JSON format');
        }
    };

    return (
        <div className="domain-purchase-container">
            <h2 className="title">Domain Purchases</h2>
            {error && <p className="error-message">{error}</p>}
            <ul className="domain-list">
                {domains.map((domain) => (
                    <li key={domain.id} className="domain-item">
                        <h3 className="domain-name">{domain.domain_name}</h3>
                        <p className="domain-contact-info">Contact Info: {JSON.stringify(domain.contact_info)}</p>
                        <input
                            className="domain-input"
                            type="text"
                            placeholder="Domain Name"
                            value={domain.domain_name}
                            readOnly
                        />
                        <textarea
                            className="contact-info-textarea"
                            placeholder="Contact Info (JSON)"
                            onChange={handleContactInfoChange}
                        />
                        <button className="update-button" onClick={() => handleUpdate(domain.domain_name)}>Update</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DomainPurchasePage;
