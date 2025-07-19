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
    SimpleGrid
} from '@chakra-ui/react';
import { AddIcon, CloseIcon, RefreshIcon } from '@chakra-ui/icons';
import { useAuth } from '../contexts/AuthContext';

const SuggestedFriends = () => {
    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const { token } = useAuth();
    const toast = useToast();

    const fetchSuggestions = async () => {
        try {
            const response = await fetch('/api/users/suggested-friends/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setSuggestions(data);
            } else {
                throw new Error('Erreur lors du chargement des suggestions');
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
                
                // Retirer l'utilisateur de la liste des suggestions
                setSuggestions(suggestions.filter(user => user.id !== userId));
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

    const refreshSuggestions = async () => {
        setRefreshing(true);
        await fetchSuggestions();
        setRefreshing(false);
    };

    useEffect(() => {
        fetchSuggestions();
    }, []);

    if (loading) {
        return (
            <Box p={4} textAlign="center">
                <Spinner size="lg" />
                <Text mt={2}>Chargement des suggestions...</Text>
            </Box>
        );
    }

    return (
        <Box p={4}>
            <VStack spacing={4} align="stretch">
                <HStack justify="space-between">
                    <Heading size="md">Suggestions d'amis</Heading>
                    <Button
                        size="sm"
                        leftIcon={<RefreshIcon />}
                        onClick={refreshSuggestions}
                        isLoading={refreshing}
                    >
                        Actualiser
                    </Button>
                </HStack>

                {suggestions.length > 0 ? (
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                        {suggestions.map((user) => (
                            <Box
                                key={user.id}
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
                                            name={user.full_name}
                                            src={user.profile_picture}
                                        />
                                        <VStack align="start" spacing={1} flex={1}>
                                            <Text fontWeight="bold" fontSize="sm">
                                                {user.full_name}
                                            </Text>
                                            <Text fontSize="xs" color="gray.600">
                                                @{user.username}
                                            </Text>
                                            {user.quartier_name && (
                                                <Badge colorScheme="blue" size="xs">
                                                    {user.quartier_name}
                                                </Badge>
                                            )}
                                        </VStack>
                                    </HStack>
                                    
                                    <Button
                                        size="sm"
                                        colorScheme="blue"
                                        leftIcon={<AddIcon />}
                                        onClick={() => followUser(user.id)}
                                        width="full"
                                    >
                                        Suivre
                                    </Button>
                                </VStack>
                            </Box>
                        ))}
                    </SimpleGrid>
                ) : (
                    <Alert status="info">
                        <AlertIcon />
                        Aucune suggestion d'ami disponible pour le moment.
                    </Alert>
                )}
            </VStack>
        </Box>
    );
};

export default SuggestedFriends; 