import React from 'react';
import styled from 'styled-components';

const LoginScreen = ({ children }: { children: React.ReactNode }) => {
  return (
    <Container>
      {children}
    </Container>
  );
};

const Container = styled.div`
  background: #aa4b6b;
  background: -webkit-repeating-radial-gradient(top left, circle, red, blue 10%, red 20%);
  background: repeating-radial-gradient(top left, circle, red, blue 10%, red 20%);
  padding: 2rem 1rem;
  color: #fff;
`;

export default LoginScreen;
