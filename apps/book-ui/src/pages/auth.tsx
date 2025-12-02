import React from 'react';
import Layout from '@theme/Layout';
import AuthForms from '@site/src/components/AuthForms';

function AuthPage() {
  return (
    <Layout
      title="Auth"
      description="Signup, Signin, and Profile Management"
    >
      <main>
        <AuthForms />
      </main>
    </Layout>
  );
}

export default AuthPage;
