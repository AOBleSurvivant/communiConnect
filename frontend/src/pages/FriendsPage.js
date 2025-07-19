import React, { useState } from 'react';
import {
    Box,
    VStack,
    HStack,
    Text,
    Heading,
    Tabs,
    TabList,
    TabPanels,
    Tab,
    TabPanel,
    Badge,
    useToast
} from '@chakra-ui/react';
import { 
    SearchIcon, 
    UserAddIcon, 
    TimeIcon, 
    UsersIcon,
    BellIcon
} from '@chakra-ui/icons';
import UserSearch from '../components/UserSearch';
import SuggestedFriends from '../components/SuggestedFriends';
import PendingFriends from '../components/PendingFriends';
import UserConnections from '../components/UserConnections';
import { useAuth } from '../contexts/AuthContext';

const FriendsPage = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [pendingCount, setPendingCount] = useState(0);
    const { user } = useAuth();
    const toast = useToast();

    const handlePendingCountUpdate = (count) => {
        setPendingCount(count);
    };

    return (
        <Box p={4} maxW="1200px" mx="auto">
            <VStack spacing={6} align="stretch">
                <Box>
                    <Heading size="lg" mb={2}>
                        Gérer mes connexions
                    </Heading>
                    <Text color="gray.600">
                        Découvrez de nouveaux utilisateurs, gérez vos demandes d'amitié et vos connexions
                    </Text>
                </Box>

                <Tabs index={activeTab} onChange={setActiveTab} variant="enclosed">
                    <TabList>
                        <Tab>
                            <HStack spacing={2}>
                                <SearchIcon />
                                <Text>Rechercher</Text>
                            </HStack>
                        </Tab>
                        <Tab>
                            <HStack spacing={2}>
                                <UserAddIcon />
                                <Text>Suggestions</Text>
                            </HStack>
                        </Tab>
                        <Tab>
                            <HStack spacing={2}>
                                <TimeIcon />
                                <Text>Demandes</Text>
                                {pendingCount > 0 && (
                                    <Badge colorScheme="red" borderRadius="full" px={2}>
                                        {pendingCount}
                                    </Badge>
                                )}
                            </HStack>
                        </Tab>
                        <Tab>
                            <HStack spacing={2}>
                                <UsersIcon />
                                <Text>Mes connexions</Text>
                            </HStack>
                        </Tab>
                    </TabList>

                    <TabPanels>
                        <TabPanel>
                            <Box>
                                <Heading size="md" mb={4}>
                                    Rechercher des utilisateurs
                                </Heading>
                                <Text mb={4} color="gray.600">
                                    Trouvez des utilisateurs par nom, prénom ou email
                                </Text>
                                <UserSearch />
                            </Box>
                        </TabPanel>

                        <TabPanel>
                            <Box>
                                <Heading size="md" mb={4}>
                                    Suggestions d'amis
                                </Heading>
                                <Text mb={4} color="gray.600">
                                    Découvrez des utilisateurs de votre quartier que vous pourriez connaître
                                </Text>
                                <SuggestedFriends />
                            </Box>
                        </TabPanel>

                        <TabPanel>
                            <Box>
                                <Heading size="md" mb={4}>
                                    Demandes d'amitié
                                </Heading>
                                <Text mb={4} color="gray.600">
                                    Gérez les demandes d'amitié que vous avez reçues
                                </Text>
                                <PendingFriends onCountUpdate={handlePendingCountUpdate} />
                            </Box>
                        </TabPanel>

                        <TabPanel>
                            <Box>
                                <Heading size="md" mb={4}>
                                    Mes connexions
                                </Heading>
                                <Text mb={4} color="gray.600">
                                    Consultez vos abonnés et abonnements
                                </Text>
                                {user && <UserConnections userId={user.id} />}
                            </Box>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </VStack>
        </Box>
    );
};

export default FriendsPage; 