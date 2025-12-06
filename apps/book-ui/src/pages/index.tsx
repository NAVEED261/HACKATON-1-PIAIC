import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import ChatbotWidget from '@site/src/components/ChatbotWidget';

import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          Physical AI & Humanoid Robotics
        </Heading>
        <p className={styles.heroSubtitle}>
          Master the future of robotics with our comprehensive AI-powered learning platform
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Learning
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro"
            style={{marginLeft: '1rem'}}>
            Browse Chapters
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <div className={styles.feature}>
              <h3>🤖 AI-Powered Learning</h3>
              <p>
                Get instant answers to your questions with our intelligent chatbot, trained on comprehensive robotics content.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.feature}>
              <h3>📚 Comprehensive Content</h3>
              <p>
                From ROS 2 basics to advanced humanoid robotics, covering everything you need to know about Physical AI.
              </p>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.feature}>
              <h3>💡 Interactive Learning</h3>
              <p>
                Engage with content through our RAG-based question-answering system for personalized learning experiences.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function TopicsSection() {
  return (
    <section className={styles.topics}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          What You'll Learn
        </Heading>
        <div className="row">
          <div className="col col--6">
            <div className={styles.topicCard}>
              <h3>ROS 2 Fundamentals</h3>
              <ul>
                <li>Core concepts and architecture</li>
                <li>Node communication patterns</li>
                <li>Real-time control systems</li>
                <li>Multi-robot coordination</li>
              </ul>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.topicCard}>
              <h3>Humanoid Robotics</h3>
              <ul>
                <li>Locomotion and balance</li>
                <li>Human-robot interaction</li>
                <li>Perception and planning</li>
                <li>Advanced AI integration</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="Learn Physical AI & Humanoid Robotics with our comprehensive AI-powered textbook">
      <HomepageHeader />
      <main>
        <FeaturesSection />
        <TopicsSection />
      </main>
      <ChatbotWidget chapterContent="Welcome to Physical AI & Humanoid Robotics! Ask me anything about robotics, ROS 2, or humanoid systems." />
    </Layout>
  );
}
