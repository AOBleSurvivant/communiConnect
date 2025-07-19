import React, { useState, useEffect } from 'react';
import { 
    Box, 
    VStack, 
    HStack, 
    Text, 
    Avatar, 
    Button, 
    Badge,
    Spinner,
    Alert,
    AlertIcon,
    useToast,
    Heading,
    Tabs,
    TabList,
    TabPanels,
    Tab,
    TabPanel,
    SimpleGrid
} from '@chakra-ui/react';
import { AddIcon, CloseIcon, ViewIcon } from '@chakra-ui/icons';
import { useAuth } from '../contexts/AuthContext';

const UserConnections = ({ userId }) => {
    const [followers, setFollowers] = useState([]);
    const [following, setFollowing] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState(0);
    const { token, user } = useAuth();
    const toast = useToast();

    const fetchFollowers = async () => {
        try {
            const response = await fetch(`/api/users/followers/${userId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setFollowers(data);
            } else {
                throw new Error('Erreur lors du chargement des abonnés');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const fetchFollowing = async () => {
        try {
            const response = await fetch(`/api/users/following/${userId}/`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setFollowing(data);
            } else {
                throw new Error('Erreur lors du chargement des abonnements');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setLoading(false);
        }
    };

    const followUser = async (userId) => {
        try {
            const response = await fetch('/api/users/follow/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId }),
            });

            if (response.ok) {
                const data = await response.json();
                toast({
                    title: 'Succès',
                    description: data.message,
                    status: 'success',
                    duration: 3000,
                    isClosable: true,
                });
                
                // Mettre à jour les listes
                fetchFollowers();
                fetchFollowing();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de l\'ajout');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const unfollowUser = async (userId) => {
        try {
            const response = await fetch('/api/users/unfollow/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId }),
            });

            if (response.ok) {
                const data = await response.json();
                toast({
                    title: 'Succès',
                    description: data.message,
                    status: 'success',
                    duration: 3000,
                    isClosable: true,
                });
                
                // Mettre à jour les listes
                fetchFollowers();
                fetchFollowing();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de la suppression');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    useEffect(() => {
        fetchFollowers();
        fetchFollowing();
    }, [userId]);

    const isOwnProfile = user?.id === userId;

    if (loading) {
        return (
            <Box p={4} textAlign="center">
                <Spinner size="lg" />
                <Text mt={2}>Chargement des connexions...</Text>
            </Box>
        );
    }

    return (
        <Box p={4}>
            <VStack spacing={4} align="stretch">
                <Heading size="md">Connexions</Heading>
                
                <Tabs index={activeTab} onChange={setActiveTab}>
                    <TabList>
                        <Tab>
                            Abonnés ({followers.length})
                        </Tab>
                        <Tab>
                            Abonnements ({following.length})
                        </Tab>
                    </TabList>
                    
                    <TabPanels>
                        <TabPanel>
                            {followers.length > 0 ? (
                                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                                    {followers.map((follower) => (
                                        <Box
                                            key={follower.id}
                                            p={4}
                                            border="1px"
                                            borderColor="gray.200"
                                            borderRadius="md"
                                            _hover={{ shadow: "md" }}
                                            transition="all 0.2s"
                                        >
                                            <VStack spacing={3} align="stretch">
                                                <HStack spacing={3}>
                                                    <Avatar
                                                        size="md"
                                                        name={follower.full_name}
                                                        src={follower.profile_picture}
                                                    />
                                                    <VStack align="start" spacing={1} flex={1}>
                                                        <Text fontWeight="bold" fontSize="sm">
                                                            {follower.full_name}
                                                        </Text>
                                                        <Text fontSize="xs" color="gray.600">
                                                            @{follower.username}
                                                        </Text>
                                                        {follower.quartier && (
                                                            <Badge colorScheme="blue" size="xs">
                                                                {follower.quartier.nom}
                                                            </Badge>
                                                        )}
                                                    </VStack>
                                                </HStack>
                                                
                                                {isOwnProfile && (
                                                    <Button
                                                        size="sm"
                                                        colorScheme="blue"
                                                        leftIcon={<ViewIcon />}
                                                        onClick={() => window.location.href = `/profile/${follower.id}`}
                                                        width="full"
                                                    >
                                                        Voir profil
                                                    </Button>
                                                )}
                                            </VStack>
                                        </Box>
                                    ))}
                                </SimpleGrid>
                            ) : (
                                <Alert status="info">
                                    <AlertIcon />
                                    Aucun abonné pour le moment.
                                </Alert>
                            )}
                        </TabPanel>
                        
                        <TabPanel>
                            {following.length > 0 ? (
                                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                                    {following.map((followed) => (
                                        <Box
                                            key={followed.id}
                                            p={4}
                                            border="1px"
                                            borderColor="gray.200"
                                            borderRadius="md"
                                            _hover={{ shadow: "md" }}
                                            transition="all 0.2s"
                                        >
                                            <VStack spacing={3} align="stretch">
                                                <HStack spacing={3}>
                                                    <Avatar
                                                        size="md"
                                                        name={followed.full_name}
                                                        src={followed.profile_picture}
                                                    />
                                                    <VStack align="start" spacing={1} flex={1}>
                                                        <Text fontWeight="bold" fontSize="sm">
                                                            {followed.full_name}
                                                        </Text>
                                                        <Text fontSize="xs" color="gray.600">
                                                            @{followed.username}
                                                        </Text>
                                                        {followed.quartier && (
                                                            <Badge colorScheme="blue" size="xs">
                                                                {followed.quartier.nom}
                                                            </Badge>
                                                        )}
                                                    </VStack>
                                                </HStack>
                                                
                                                <HStack spacing={2}>
                                                    <Button
                                                        size="sm"
                                                        colorScheme="blue"
                                                        leftIcon={<ViewIcon />}
                                                        onClick={() => window.location.href = `/profile/${followed.id}`}
                                                        flex={1}
                                                    >
                                                        Voir profil
                                                    </Button>
                                                    
                                                    {isOwnProfile && (
                                                        <Button
                                                            size="sm"
                                                            colorScheme="red"
                                                            variant="outline"
                                                            leftIcon={<CloseIcon />}
                                                            onClick={() => unfollowUser(followed.id)}
                                                        >
                                                            Ne plus suivre
                                                        </Button>
                                                    )}
                                                </HStack>
                                            </VStack>
                                        </Box>
                                    ))}
                                </SimpleGrid>
                            ) : (
                                <Alert status="info">
                                    <AlertIcon />
                                    Aucun abonnement pour le moment.
                                </Alert>
                            )}
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </VStack>
        </Box>
    );
};

export default UserConnections; 